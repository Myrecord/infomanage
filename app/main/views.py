# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template, jsonify, redirect, url_for, flash, current_app, send_from_directory,Response
from script.push_cdn import pushcdn
from flask import request,abort
from sqlalchemy import func, or_
from .. import db
from ..models import Hosts, Groupname, Grouphostid, User, Menu, Tasks, Filename, Logs, Role,datastore
from . import main
from flask_login import login_required, current_user
from datetime import *
import os, re
from .. import scheduler
import pickle
from script.oss import Ossoperation
from app import sockets
from script.webssh_conncet import Remote
from script.hosts import hostinfo
import threading
from functools import wraps

online_user = []
@main.before_request
@login_required
def online_users():
    if current_user.username not in online_user:
        online_user.append(current_user.username)
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for login_user in online_user:
        user_last_time = db.session.query(User).filter(User.username == login_user).first()
        user_last_time = (user_last_time.last_time + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        if user_last_time < now_time:
             online_user.remove(login_user)

def permission(routes):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            permission_list = []
            user_permission = db.session.query(User.id.label('id'), Role.permission.label('permission'))\
                .join(Role,User.rolesid == Role.id)\
                .filter( User.username == current_user.username ).first()
            status = True
            for permission in user_permission.permission.split(','):
                user_url = db.session.query(Menu).filter(Menu.id == permission).first()
                permission_list.append(user_url.url)
            if routes not in permission_list:
                status = False
            res = func(status,*args, **kwargs)
            return res
        return wrapper
    return decorator


@main.route('/')
@main.route('/index')
@login_required
def index():
    with open(os.path.join(current_app.config['SCRIPT_LOCAL_PATH'],'grouping_host_count'),'r') as files:
        grouping_host_count = pickle.load(files)
    onlien_user_count = len(online_user)
    host_count = db.session.query(Hosts.id).count()
    user_count = db.session.query(User.id).count()
    return render_template('index.html',
                           host_count = host_count,
                           user_count = user_count,
                           onlien_user_count = onlien_user_count,
                           grouping_host_count = grouping_host_count,
                           domain_ranping = pushcdn().get_domain())

@main.route('/checkip', methods=['GET', 'POST'])
@login_required
@permission('checkip')
def checkip(permission_status):
    if permission_status:
        client_ip = request.remote_addr
        return render_template('checkip.html', client_ip=client_ip)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))


@main.route('/loadcdn', methods=['GET', 'POST'])
@login_required
@permission('loadcdn')
def loadcdn(permission_status):
    if permission_status:
        all_info = pushcdn()
        return render_template('cdn.html',number=all_info.selectnumber(),records_info=all_info.records())
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))


@main.route('/cdndata', methods=['GET', 'POST'])
@login_required
@permission('cdndata')
def cdndata(permission_status):
    if permission_status:
        if request.method == 'POST':
            all_info = pushcdn()
            action = request.form.get('action')
            types = request.form.get('types')
            httpurl = request.form.get('httpurl')
            try:
                if action == 'refresh' or types == 'directory':
                    all_info.refredomain(httpurl, types)
                    userlog(current_user.username, request.remote_addr, '预热CDN')
                elif action == 'push':
                    all_info.pushdomain(httpurl)
                    userlog(current_user.username, request.remote_addr, '刷新CDN')
            except Exception as e:
                flash('%s' % e)
            else:
                flash('Success: %s' % httpurl)
        return redirect(url_for('main.loadcdn'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.loadcdn'))


@main.route('/osslist', methods=['GET', 'POST'])
@login_required
@permission('osslist')
def osslist(permission_status):
    if permission_status:
        chdirs = request.values.get('path')
        with open(os.path.join(current_app.config['SCRIPT_LOCAL_PATH'],'oss_obj_info'),'r') as files:
            ossobject = pickle.load(files)
        if chdirs:
            return render_template('ossfile.html',ossobject=ossobject,chdirs=chdirs)
        return render_template('osslist.html',ossobject = ossobject)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@main.route('/oss_upfile', methods=['GET', 'POST'])
@login_required
@permission('oss_upfile')
def oss_upfile(permission_status):
    if permission_status:
        dirname = request.values.get('path')
        try:
            upload_oss_files = Ossoperation()
            for i in request.files:
                files_name = request.files[i]
                files_name.save(os.path.join(current_app.config['UPLOADED_FILE_DEST'], files_name.filename))
                upload_oss_files.upload_files(dirname+'/'+ files_name.filename,
                                              os.path.join(current_app.config['UPLOADED_FILE_DEST'],files_name.filename))
            userlog(current_user.username, request.remote_addr, '上传文件(OSS)')
        except Exception as e:
            raise e
        return redirect(url_for('main.osslist'))
    return Response(status=500)


@main.route('/update', methods=['GET', 'POST'])
@login_required
@permission('update')
def update(permission_status):
    if permission_status:
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Tasks).order_by(Tasks.id.desc()).paginate(page, per_page=6)
        group_record = pagination.items
        return render_template('update.html', pagination=pagination, group_record=group_record)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

def jobs(area, version, types):
    print area, version, types


@main.route('/updatedata', methods=['GET', 'POST'])
@login_required
@permission('updatedata')
def updatedata(permission_status):
    if permission_status:
        if request.method == 'POST':
            types = request.form.get('types')
            area = request.form.get('areas')
            version = request.form.get('version')
            dates = request.form.get('dates')
            if types and area and version:
                if dates or not dates:
                    try:
                        areas = area.split(' ')[0] if types == 'server' else area.split(' ')[1]
                        new_task = Tasks(
                            user=current_user.username,
                            area=areas,
                            types=types,
                            version=version,
                            dates=dates,
                        )
                        db.session.add(new_task)
                        db.session.commit()
                        scheduler.add_job(
                            func=jobs,
                            trigger='date',
                            run_date=dates,
                            id=dates,
                            args=(areas, version, types))
                        userlog(current_user.username, request.remote_addr,'添加更新任务')
                    except:
                        db.session.rollback()
                    db.session.close()
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.update'))


@main.route('/deljobs', methods=['GET', 'POST'])
@login_required
@permission('deljobs')
def deljobs(permission_status):
    if permission_status:
        if request.method == 'POST':
            try:
                db.session.query(Tasks).filter(
                    Tasks.id == request.form.get('id')).delete()
                db.session.commit()
                scheduler.remove_job(request.form.get('name'))
                userlog(current_user.username, request.remote_addr, '删除更新任务')
                flash('已删除此任务')
            except Exception as e:
                flash('发生错误：%s' % e)
            status = {'status': 'success'}
            return jsonify(status)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.update'))


@main.route('/log', methods=['GET', 'POST'])
@login_required
@permission('log')
def logs(permission_status):
    if permission_status:
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Logs).filter(Logs.user == current_user.username)\
            .order_by(Logs.id.desc()).paginate(page, per_page=13)
        user_log = pagination.items
        return render_template(
            'logs.html', user_log=user_log, pagination=pagination)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@login_required
def userlog(user, ip, strs):
    dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        userinfo = Logs(user=user, address=ip, datetime=dates, strs=strs)
        db.session.add(userinfo)
        db.session.commit()
    except:
        db.session.rollback()


@main.route('/host', methods=['GET', 'POST'])
@login_required
@permission('host')
def host(permission_status):
    if permission_status:
        page = request.args.get('page', 1, type=int)
        subinfo = request.args.get('hostsearch')
        if subinfo:
            groupnames = db.session.query(Groupname.id, Groupname.name)
            page = request.args.get('page', 1, type=int)
            pagination = db.session.query(
                Hosts,
                func.group_concat(Groupname.name).label('names')) \
                .join(Grouphostid, Hosts.id == Grouphostid.hostid,isouter=True) \
                .join(Groupname,Groupname.id == Grouphostid.groupid,isouter=True) \
                .filter(or_(
                Hosts.netip.like('%' + subinfo + '%'),
                Hosts.area.like('%' + subinfo + '%'),
                Hosts.name.like('%' + subinfo + '%')
            )).group_by(Hosts.id).paginate(page, per_page=10)
            hostinfo = pagination.items
            return render_template('host.html',
                                   groupnames=groupnames,
                                   hostinfo=hostinfo,
                                   subinfo=subinfo,
                                   pagination=pagination,
                                   error_out=True)
        groupnames = db.session.query(Groupname.id, Groupname.name)
        pagination = db.session.query(
            Hosts,
            func.group_concat(Groupname.name).label('names')) \
            .join(Grouphostid, Hosts.id == Grouphostid.hostid, isouter=True) \
            .join(Groupname, Groupname.id == Grouphostid.groupid,isouter=True) \
            .group_by(Hosts.id).order_by(Hosts.id.desc()).paginate(page, per_page=10)
        hostinfo = pagination.items
        return render_template('host.html',groupnames=groupnames,hostinfo=hostinfo,pagination=pagination,subinfo=subinfo)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))


@main.route('/addhost', methods=['GET', 'POST'])
@login_required
@permission('addhost')
def addhost(permission_status):
    if permission_status:
        if request.method == 'POST':
            try:
                netip = request.form.get('address'),
                new_host = Hosts(
                    netip=request.form.get('address'),
                    name=request.form.get('name'),
                    area=request.form.get('area'),
                    osname=request.form.get('nameos'),
                    cpuinfo=request.form.get('cpu'),
                    internet=request.form.get('net'),
                    memory=request.form.get('memory'))
                db.session.add(new_host)
                add_group = request.form.getlist('add_group')
                new_hostid = db.session.query(Hosts.id).filter(Hosts.netip == netip).first()
                if add_group:
                    for i in add_group:
                        new_info = Grouphostid(groupid=i, hostid=new_hostid[0])
                        db.session.add(new_info)
                db.session.commit()
                userlog(current_user.username, request.remote_addr, '添加主机')
            except Exception as e:
                db.session.rollback()
            finally:
                db.session.close()
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.host'))


@main.route('/websshs', methods=['GET', 'POST'])
@permission('websshs')
def websshs(permission_status):
    if permission_status:
        connect_ip = request.values.get('ID')
        global connect_ip
        return render_template('webssh.html',ID=connect_ip)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.host'))

class sshTherad(threading.Thread):

    def __init__(self, ws,connect):
        threading.Thread.__init__(self)
        self.ws = ws
        self.connect = connect

    def run(self):
        while not self.ws.closed:
            try:
                sava_connect = self.connect.recv(4096)
                if sava_connect is not None:
                    self.ws.send(sava_connect)
                else:
                    self.ws.close()
            except Exception as e:
                print e
        self.ws.close()

@sockets.route('/echo')
def xterm_web(ws):
    ssh = Remote()
    sava_connect = ssh.ssh_connect(connect_ip,'',current_user.username)
    if sava_connect:
        userlog(current_user.username, request.remote_addr, '登录服务器 %s' % connect_ip)
        Thread_connect = sshTherad(ws,sava_connect)
        Thread_connect.start()
        while not ws.closed:
            message = ws.receive()
            if message is not None:
                sava_connect.sendall(message)
    sava_connect.close()


@main.route('/deletehost', methods=['GET', 'POST'])
@login_required
@permission('deletehost')
def deletehost(permission_status):
    if permission_status:
        remove = request.form.get('id')
        if request.method == 'POST' and remove:
            try:
                db.session.query(Hosts).filter(Hosts.id == remove).delete()
                db.session.query(Grouphostid).filter(
                    Grouphostid.hostid == remove).delete()
                db.session.commit()
            except:
                db.session.rollback()
            else:
                status = {
                    'status': 'success',
                }
                userlog(current_user.username, request.remote_addr, '删除主机')
            return jsonify(status)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.host'))


@main.route('/edithost', methods=['GET', 'POST'])
@login_required
@permission('edithost')
def edithost(permission_status):
    if permission_status:
        if request.method == 'POST':
            new_info = Hosts.query.filter_by(id=request.form.get('ids')).all()
            for i in new_info:
                i.netip = request.form.get('netips')
                i.name = request.form.get('names')
                i.area = request.form.get('areas')
                i.osname = request.form.get('osnames')
                i.internet = request.form.get('internets')
                i.cpuinfo = request.form.get('cpuinfos')
                i.memory = request.form.get('memorys')
                db.session.add(i)
                jsondata = {
                    'id': i.id,
                    'netip': i.netip,
                    'name': i.name,
                    'area': i.area,
                    'osname': i.osname,
                    'internet': i.internet,
                    'cpuinfo': i.cpuinfo,
                    'memory': i.memory,
                }
            userlog(current_user.username, request.remote_addr, '编辑主机')
            return jsonify(jsondata)
    return Response(status=500)

@main.route('/sync_data', methods=['GET', 'POST'])
@login_required
@permission('sync_data')
def sync_data(permission_status):
    if permission_status:
        try:
            db.session.query(Hosts).delete()
            hostinfos = hostinfo()
            for i in sum(hostinfos.get_host(),[]):
                print i['PublicIpAddress']['IpAddress'][0]
                info = Hosts(netip=i['PublicIpAddress']['IpAddress'][0],
                        name=i['InstanceName'],
                        area=i['RegionId'],
                        internet=i['InternetMaxBandwidthOut'],
                        cpuinfo=i['Cpu'],
                        memory=i['Memory'])
                db.session.add(info)
            db.session.commit()
            status = {
                'status': 'success',
            }
            flash('更新信息成功')
            userlog(current_user.username, request.remote_addr, '更新主机信息')
            hostinfos.grouping_count()
            return jsonify(status)
        except Exception as e:
            print e
    return Response(status=500)

@main.route('/hostgroup', methods=['GET', 'POST'])
@login_required
@permission('hostgroup')
def hostgroup(permission_status):
    if permission_status:
        page = request.args.get('page', 1, type=int)
        groupsearch = request.args.get('groupsearch')
        if groupsearch:
            pagination = db.session.query(
                Groupname.id.label('id'),
                Groupname.name.label('name'),
                func.count(Grouphostid.hostid).label('count'),
                Groupname.comment.label('comment')) \
                .join(Grouphostid, Groupname.id == Grouphostid.groupid,isouter=True) \
                .group_by(Groupname.id) \
                .filter(Groupname.name.like('%' + groupsearch + '%')).paginate(page, per_page=10)
            groups = pagination.items
            return render_template('hostgroup.html',groupsearch=groupsearch,groups=groups,pagination=pagination)
        pagination = db.session.query(
            Groupname.id.label('id'),
            Groupname.name.label('name'),
            func.count(Grouphostid.hostid).label('count'),Groupname.comment.label('comment')) \
            .join(Grouphostid, Groupname.id == Grouphostid.groupid,isouter=True) \
            .group_by(Groupname.id).paginate(page, per_page=10)
        groups = pagination.items
        return render_template('hostgroup.html', groups=groups, pagination=pagination)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))


@main.route('/groupadd', methods=['GET', 'POST'])
@login_required
@permission('groupadd')
def groupadd(permission_status):
    if permission_status:
        if request.method == 'POST':
            listid = request.form.getlist('groupip')
            name = request.form.get('names')
            comment = request.form.get('caomm')
            try:
                groupname = Groupname(name=name, comment=comment)
                db.session.add(groupname)
                groupid = Groupname.query.filter_by(name=name).first()
                for i in listid:
                    addid = Grouphostid(groupid=groupid.id, hostid=i)
                    db.session.add(addid)
                    hostids = Hosts.query.filter_by(id=i).first()
                db.session.commit()
                flash('添加主机组成功')
                userlog(current_user.username, request.remote_addr, '添加主机组')
            except:
                pass
        allhost = db.session.query(Hosts.id, Hosts.netip, Hosts.name).all()
        return render_template('groupadd.html', allhost=allhost)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.hostgroup'))


@main.route('/editgroup', methods=['GET', 'POST'])
@login_required
@permission('editgroup')
def editgroup(permission_status):
    if permission_status:
        if request.method == 'POST':
            groupid = request.form.get('id')
            listid = request.form.getlist('groupip')
            name = request.form.get('names')
            comment = request.form.get('caomm')
            assets = request.form.getlist('assets')
            try:
                group = Groupname.query.filter_by(id=groupid).first()
                group.name = name
                group.comment = comment
                db.session.commit()
                if listid:
                    for i in listid:
                        addids = Grouphostid(groupid=groupid, hostid=i)
                        db.session.add(addids)
                elif assets:
                    for dell in assets:
                        dell_hostid = Grouphostid.query.filter_by(groupid=groupid, hostid=dell).first()
                        db.session.delete(dell_hostid)
                db.session.commit()
                flash('编辑主机组成功')
                userlog(current_user.username, request.remote_addr, '编辑主机组')
            except:
                db.session.rollback()
            finally:
                db.session.close()
        groupid = request.args.get('groupid')
        groupinfo = Groupname.query.filter_by(id=groupid).first()
        hostinfo = db.session.query(Hosts.id, Hosts.netip, Hosts.name)\
            .filter(Grouphostid.hostid == Hosts.id).filter(Grouphostid.groupid == groupid)
        get_host = db.session.query(Grouphostid.hostid).filter(Grouphostid.groupid == groupid)
        alldata = db.session.query(Hosts.id, Hosts.name,Hosts.netip).filter(~Hosts.id.in_(get_host))
        return render_template('editgroup.html', hostinfo=hostinfo, groupinfo=groupinfo, alldata=alldata)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.hostgroup'))



@main.route('/deletegroup', methods=['GET', 'POST'])
@login_required
@permission('deletegroup')
def deletegroup(permission_status):
    if permission_status:
        groupids = request.form.get('id')
        if request.method == 'POST' and groupids:
            try:
                db.session.query(Groupname).filter(Groupname.id == groupids).delete()
                db.session.query(Grouphostid).filter(Grouphostid.groupid == groupids).delete()
                db.session.commit()
                flash('删除主机组成功')
                userlog(current_user.username, request.remote_addr, '删除主机组')
                status = {
                'status': 'success',
                }
                return jsonify(status)
            except Exception as e:
                db.session.rollback()
            return redirect(url_for('main.hostgroup'))
    return Response(status=500)

@main.route('/datastores')
@login_required
@permission('datastores')
def datastores(permission_status):
    if permission_status:
        page = request.args.get('page', 1, type=int)
        if request.values.get('datasearch'):
            pagination = db.session.query(datastore).filter(or_(
                datastore.name.like('%' + request.values.get('datasearch') + '%'),
                datastore.netip.like('%' + request.values.get('datasearch') + '%'))).paginate(page, per_page=10)
            datainfo = pagination.items
            return render_template('datastore.html', datainfo=datainfo, pagination=pagination)
        pagination = db.session.query(datastore).paginate(page,per_page=10)
        datainfo = pagination.items
        return render_template('datastore.html',datainfo = datainfo,pagination = pagination)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@main.route('/editdatas',methods=['GET','POST'])
@login_required
@permission('editdatas')
def editdatas(permission_status):
    if permission_status:
        if request.method == 'POST':
            new_data = datastore.query.filter_by(id=request.form.get('ids')).all()
            try:
                for data in new_data:
                    data.netip = request.form.get('netip')
                    data.port = request.form.get('port')
                    data.cpu = request.form.get('cpu')
                    data.memory = request.form.get('memory')
                    data.name = request.form.get('name')
                    data.area = request.form.get('area')
                    data.version = request.form.get('version')
                    data.connect_number = request.form.get('connect_number')
                    data.types = request.form.get('types')
                    db.session.add(data)
                    flash('编辑成功')
                    userlog(current_user.username, request.remote_addr, '编辑数据库信息')
                db.session.commit()
            except Exception as e:
                raise e
        return redirect(url_for('main.datastores'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.datastores'))

@main.route('/deldatas',methods=['GET','POST'])
@login_required
@permission('deldatas')
def deldatas(permission_status):
    if permission_status:
        if request.values.get('ids'):
            try:
                delinfo = datastore.query.filter(datastore.id == request.values.get('ids')).first()
                db.session.delete(delinfo)
                db.session.commit()
                flash('删除成功')
                userlog(current_user.username, request.remote_addr, '删除数据库信息')
            except Exception as e:
                raise e
        return redirect(url_for('main.datastores'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.datastores'))

@main.route('/adddatas',methods=['GET','POST'])
@login_required
@permission('adddatas')
def adddatas(permission_status):
    if permission_status:
        if request.method == 'POST':
            try:
                new_data = datastore(
                    netip=request.form.get('netip'),
                    port=request.form.get('port'),
                    cpu=request.form.get('cpu'),
                    memory=request.form.get('memory'),
                    name=request.form.get('name'),
                    area=request.form.get('area'),
                    types=request.form.get('types'),
                    version=request.form.get('version'),
                    connect_number=request.form.get('connect_number')
                )
                db.session.add(new_data)
                db.session.commit()
                flash('添加数据信息成功')
                userlog(current_user.username, request.remote_addr, '添加数据库信息')
            except Exception as e:
                raise e
        return redirect(url_for('main.datastores'))
    return Response(status=500)


@main.route('/listfile', methods=['GET', 'POST'])
@login_required
@permission('listfile')
def listfile(permission_status):
    if permission_status:
        filesearch = request.args.get('filesearch')
        page = request.args.get('page', 1, type=int)
        if filesearch:
            pagination = db.session.query(Filename)\
                .filter(Filename.name.like('%' + filesearch + '%')).paginate(page, per_page=10)
            files_list = pagination.items
            return render_template('listfile.html', pagination=pagination, files_list=files_list)
        pagination = db.session.query(Filename).order_by(Filename.id.desc()).paginate(page, per_page=10)
        files_list = pagination.items
        return render_template('listfile.html', pagination=pagination, files_list=files_list)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@main.route('/fileload', methods=['GET', 'POST'])
@login_required
@permission('fileload')
def fileload(permission_status):
    if permission_status:
        if request.method == 'POST':
            filetype = ['xlsx', 'xls', 'zip', 'tar', 'pub', 'txt']
            for i in request.files:
                f = request.files[i]
                if f.filename.split('.')[1] not in filetype:
                    return 'Error', 400
                try:
                    new_file = Filename(name=f.filename)
                    db.session.add(new_file)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return '文件名称重复', 500
                userlog(current_user.username, request.remote_addr, '文件上传')
                f.save(os.path.join(current_app.config['UPLOADED_FILE_DEST'],f.filename))
        return render_template('fileload.html')
    return Response(status=500)


@main.route('/downfile/<filename>')
@login_required
@permission('downfile')
def downfile(permission_status,filename):
    if permission_status:
        files_list = os.listdir(current_app.config['UPLOADED_FILE_DEST'])
        userlog(current_user.username, request.remote_addr, '文件下载')
        return send_from_directory(
            current_app.config['UPLOADED_FILE_DEST'], filename, as_attachment=True)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.listfile'))

@main.route('/filedel/<filename>/<file_id>')
@login_required
@permission('filedel')
def filedel(permission_status,filename, file_id):
    if permission_status:
        db.session.query(Filename).filter(Filename.id == file_id).delete()
        os.remove(os.path.join(current_app.config['UPLOADED_FILE_DEST'], filename))
        userlog(current_user.username, request.remote_addr, '删除文件')
        return redirect(url_for('main.listfile'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.listfile'))


@main.route('/users', methods=['GET', 'POST'])
@login_required
@permission('users')
def users(permission_status):
    if permission_status:
        search_user = request.args.get('search_user')
        page = request.args.get('page', 1, type=int)
        if search_user:
            pagination = db.session.query(User)\
                .filter(User.username.like('%' + search_user + '%')).paginate(page, per_page=11)
            user_all = pagination.items
            return render_template('users.html', user_all = user_all,pagination = pagination)
        pagination = db.session.query(User).filter(~User.username.in_(['123123'])).paginate(page, per_page=11)
        user_all = pagination.items
        return render_template('users.html',user_all = user_all,pagination = pagination)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@main.route('/edituser', methods=['GET', 'POST'])
@login_required
@permission('edituser')
def edituser(permission_status):
    if permission_status:
        rolename = db.session.query(Role).all()
        edituser = request.values.get('users')
        if request.method == 'POST':
            new_pass = request.form.get('confirm_password')
            edituser_post = request.form.get('username')
            print edituser_post
            try:
                checkuser = User.query.filter_by(username = edituser_post).first()
                checkuser.password = new_pass
                db.session.commit()
                flash('用户密码修改成功')
                userlog(current_user.username, request.remote_addr, '修改用户密码')
                return redirect(url_for('main.users'))
            except Exception as e:
                flash(e)
        return render_template('edituser.html', rolename=rolename, edituser=edituser)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.users'))

@main.route('/useradd', methods=['GET', 'POST'])
@login_required
@permission('useradd')
def useradd(permission_status):
    if permission_status:
        if request.method == 'POST':
            roles = request.form.get('roles')
            try:
                adduser = User(
                    username = request.form.get('username'),
                    password= request.form.get('passwd'),
                    email = request.form.get('email'),
                    status = True,
                    last_time = datetime.now(),
                    roles = roles.split(' ')[0],
                    rolesid = roles.split(' ')[1]
                )
                db.session.add(adduser)
                db.session.commit()
                flash('创建用户成功')
                userlog(current_user.username, request.remote_addr, '创建新用户')
                return redirect(url_for('main.users'))
            except Exception as e:
                flash(e)
        rolename = db.session.query(Role).all()
        return render_template('useradd.html',rolename=rolename)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.users'))

@main.route('/deluser', methods=['GET', 'POST'])
@login_required
@permission('deluser')
def deluser(permission_status):
    if permission_status:
        if request.method == 'POST':
            try:
                userid = request.form.get('id')
                db.session.query(User.id).filter(User.id == userid).delete()
                db.session.commit()
                flash('删除用户成功')
                userlog(current_user.username, request.remote_addr, '删除用户')
                status = {
                'status': 'success',
                }
                return jsonify(status)
            except:
                flash('删除用户失败')
        return redirect(url_for('main.users'))
    return Response(status=500)


@main.route('/role', methods=['GET', 'POST'])
@login_required
@permission('role')
def role(permission_status):
    if permission_status:
        rolesearch = request.args.get('rolesearch')
        page = request.args.get('page', 1, type=int)
        if rolesearch:
            pagination = db.session.query(Role).filter(Role.name.like('%' + rolesearch + '%')).paginate(page, per_page=10)
            role_all = pagination.items
            return render_template('role.html',role_all = role_all,pagination = pagination)
        pagination = db.session.query(Role).paginate(page, per_page=10)
        role_all = pagination.items
        return render_template('role.html',role_all = role_all,pagination = pagination)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))

@main.route('/addrole', methods=['GET', 'POST'])
@login_required
@permission('addrole')
def addrole(permission_status):
    if permission_status:
        if request.method == 'POST':
            try:
                rolename = request.form.get('rolename')
                roleid = request.form.get('idlist')
                new_role = Role(
                    name = rolename,
                    permission = roleid[:-1],
                )
                db.session.add(new_role)
                db.session.commit()
                flash('添加角色成功')
                userlog(current_user.username, request.remote_addr, '添加角色')
                status = {
                'status': 'success',
                }
                return jsonify(status)
            except Exception as e:
                flash(e)
        menuall = db.session.query(Menu).all()
        return render_template('addrole.html',menuall=menuall)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.role'))

@main.route('/editrole', methods=['GET', 'POST'])
@login_required
@permission('editrole')
def editrole(permission_status):
    if permission_status:
        if request.method == 'POST':
            roleid = request.form.get('ids')
            editid_list = request.form.get('idlist')
            try:
                new_roleid = Role.query.filter(Role.id == roleid).first()
                new_roleid.permission = editid_list[:-1]
                db.session.commit()
                flash('编辑角色成功')
                userlog(current_user.username, request.remote_addr, '编辑角色')
                status = {
                'status': 'success',
                }
                return jsonify(status)
            except Exception as e:
                flash(e)
        roleid = request.args.get('edit_id')
        menuall = db.session.query(Menu).all()
        rolename = db.session.query(Role).filter_by(id = roleid).first()
        return render_template('editrole.html',menuall=menuall,rolename = rolename)
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.role'))



@main.route('/delrole', methods=['GET', 'POST'])
@login_required
@permission('delrole')
def delrole(permission_status):
    if permission_status:
        try:
            roleid = request.args.get('roleid')
            db.session.query(Role.id).filter(Role.id == roleid).delete()
            db.session.commit()
            flash('删除角色成功')
            userlog(current_user.username, request.remote_addr, '删除角色')
        except Exception as e:
            flash(e)
        return redirect(url_for('main.role'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.role'))

@main.route('/menu', methods=['GET', 'POST'])
@login_required
@permission('menu')
def menu(permission_status):
    if permission_status:
        menuall = db.session.query(Menu).all()
        return render_template('menu.html', menuall=menuall)
    else:
        flash('Error: 没有权限查看')
    return redirect(url_for('main.index'))


@main.route('/addmenu', methods=['GET', 'POST'])
@login_required
@permission('addmenu')
def addmenu(permission_status):
    if permission_status:
        if request.method == 'POST':
            new_url = Menu(
                submenuId=request.form.get('submenuid'),
                name=request.form.get('name'),
                url=request.form.get('url'),
                level=request.form.get('level'),
                flag=request.form.get('flag'))
            db.session.add(new_url)
        return redirect(url_for('main.menu'))
    else:
        flash('Error: 没有权限操作')
    return redirect(url_for('main.menu'))