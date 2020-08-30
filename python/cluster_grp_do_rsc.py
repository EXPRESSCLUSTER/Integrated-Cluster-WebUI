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
    grpname = args[2]

    # do = depends on
    url_grp_do_rsc = '{0}://{1}:{2}/api/v1/groups/{3}?select=resources'.format(method, host, port, grpname) 

    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_grp_do_rsc = urllib2.Request(url=url_grp_do_rsc, headers=headers)

    #get resources depends on group
    res_grp_do_rsc = urllib2.urlopen(req_grp_do_rsc)
    json_str_grp_do_rsc = res_grp_do_rsc.read()
    json_dict_grp_do_rsc = json.loads(json_str_grp_do_rsc)

    # result check
    rtn_code = int(json_dict_grp_do_rsc['result']['code'])
    if rtn_code != 0:
        print('get resources depends on group abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_grp_do_rsc['result']['message']))
        sys.exit()

    for i in range(len(json_dict_grp_do_rsc['groups'][0]['resources'])):
        name = '{:<32}'.format(json_dict_grp_do_rsc['groups'][0]['resources'][i]['name'])
        print('{0}'.format(name))
	
except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()

