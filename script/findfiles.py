#-*- coding: utf-8 -*
import os,sys

def Fandfile(area,filename):
    if area and filename:
        for paths,dirs,files in os.walk(area):
            if filename in dirs:
                return True
            elif filename in files:
                return True

    