#-*- coding: utf-8 -*
from app import create_app,db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import Hosts, Groupname, Grouphostid, User, Menu, Tasks ,Filename,Logs,Role,datastore


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(
        app=app,
        db=db,
        Hosts=Hosts,
        Groupname=Groupname,
        Grouphostid=Grouphostid,
        User=User,
        Menu=Menu,
        Tasks=Tasks,
	Filename=Filename,
        Logs=Logs,
        Role=Role,
	datastore=datastore,
        )

# with app.app_context():
#     hostinfo = hostinfo()
#     for i in sum(hostinfo.get_host(),[]):
#         info = Hosts(netip=i['PublicIpAddress']['IpAddress'][0],
#                 name=i['InstanceName'],
#                 area=i['RegionId'],
#                 internet=i['InternetMaxBandwidthOut'],
#                 cpuinfo=i['Cpu'],
#                 memory=i['Memory'])
#         db.session.add(info)
#     db.session.commit()

#
# with app.app_context():
#     datainfo = datainfo()
#     for i in sum(datainfo.DBinfo,[]):
#         info = datastore(netip=i['ConnectionString'],
#                          port=i['Port'],
#                          cpu=i['DBInstanceCPU'],
#                          memory=i['DBInstanceMemory'],
#                          name=i['DBInstanceDescription'],
#                          area=i['RegionId'],
#                          types=i['Engine'],
#                          version=i['EngineVersion'],
#                          connect_number=i['MaxConnections'])
#         db.session.add(info)
#     db.session.commit()
#
# with app.app_context():
#     datainfo = datainfo()
#     for i in sum(datainfo.DBinfo,[]):
#         info = datastore(netip=i['ConnectionDomain'],
#                          port=i['Port'],
#                          cpu=None,
#                          memory=i['Capacity'],
#                          name=i['InstanceName'],
#                          area=i['RegionId'],
#                          types=i['InstanceType'],
#                          version=i['EngineVersion'],
#                          connect_number=i['Connections'])
#         db.session.add(info)
#     db.session.commit()

# with app.app_context():
#     datainfo = datainfo()
#     for i in sum(datainfo.DBinfo,[]):
#         info = datastore(netip=None,
#                          port=None,
#                          cpu=None,
#                          memory=None,
#                          name=None,
#                          area=i['RegionId'],
#                          types=i['Engine'],
#                          version=i['EngineVersion'],
#                          connect_number=None)
#         db.session.add(info)
#     db.session.commit()

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    #sockets.run(app,host='127.0.0.1',port=5000,debug=True)
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    #
    # server = pywsgi.WSGIServer(('192.168.3.73', 5000), app, handler_class=WebSocketHandler)
    # print("web server start ... ")
    # server.serve_forever()
