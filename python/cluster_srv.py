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

    url_srv = '{0}://{1}:{2}/api/v1/servers'.format(method, host, port) 

    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_srv_sts = urllib2.Request(url=url_srv, headers=headers)

    #get servers status
    res_srv_sts = urllib2.urlopen(req_srv_sts)
    json_str_srvsts = res_srv_sts.read()
    json_dict_srvsts = json.loads(json_str_srvsts)
    # result check
    rtn_code = int(json_dict_srvsts['result']['code'])
    if rtn_code != 0:
        print('get server status abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_srvsts['result']['message']))
        sys.exit()

    # print data
    # server status
    for i in range(len(json_dict_srvsts['servers'])):
        name = '{:<64}'.format(json_dict_srvsts['servers'][i]['name'])
        sts = json_dict_srvsts['servers'][i]['status']
        print('{0}:{1}'.format(name, sts))
except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()

