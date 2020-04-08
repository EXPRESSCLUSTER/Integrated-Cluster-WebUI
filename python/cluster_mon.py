# -*- coding: utf-8 -*-
import urllib2, httplib
import json
import sys, os, traceback
import time, datetime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")
try:
    args = sys.argv
    method = config.get(args[1], "method")
    user = config.get(args[1], "user")
    pwd = config.get(args[1], "pwd")
    host = config.get(args[1], "host")
    port = config.get(args[1], "port")

    url_mon = '{0}://{1}:{2}/api/v1/monitors'.format(method, host, port) 

    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_mon_sts = urllib2.Request(url=url_mon, headers=headers)

    #get monitor status
    res_mon_sts = urllib2.urlopen(req_mon_sts)
    json_str_monsts = res_mon_sts.read()
    json_dict_monsts = json.loads(json_str_monsts)
    # result check
    rtn_code = int(json_dict_monsts['result']['code'])
    if rtn_code != 0:
        print('get monitor status abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_monsts['result']['message']))
        sys.exit()

    # print data
    for i in range(len(json_dict_monsts['monitors'])):
        # monitor total status
        name = '{:<32}'.format(json_dict_monsts['monitors'][i]['name'])
        tosts = json_dict_monsts['monitors'][i]['status']
        print('{0}:{1}'.format(name,tosts))
        
        # monitor status by server
        for j in range(len(json_dict_monsts['monitors'][i]['servers'])):
            srvname = '{:<32}'.format(json_dict_monsts['monitors'][i]['servers'][j]['name'])
            sts = json_dict_monsts['monitors'][i]['servers'][j]['status']
            print('{0}:{1}'.format(srvname, sts))
except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()

