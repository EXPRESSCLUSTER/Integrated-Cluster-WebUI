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
  
    url_cls = '{0}://{1}:{2}/api/v1/cluster'.format(method, host, port) 
    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_cls_sts = urllib2.Request(url=url_cls, headers=headers)

    #get cluster status
    res_cls_sts = urllib2.urlopen(req_cls_sts)
    json_str_clssts = res_cls_sts.read()
    json_dict_clssts = json.loads(json_str_clssts)
    # result check
    rtn_code = int(json_dict_clssts['result']['code'])
    if rtn_code != 0:
        print('get cluster status abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_clssts['result']['message']))
        sys.exit()

    # print data
    # cluster status
    name = '{:<32}'.format(json_dict_clssts['cluster']['name'])
    sts = json_dict_clssts['cluster']['status']
    print('{0}:{1}'.format(name, sts))
except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()

