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
    rscname = args[2]

    url_rsc = '{0}://{1}:{2}/api/v1/resources/{3}'.format(method, host, port, rscname) 
    url_srv_select = '{0}://{1}:{2}/api/v1/servers?select=name'.format(method, host, port)

    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_srv_list = urllib2.Request(url=url_srv_select, headers=headers)
    req_rsc_sts = urllib2.Request(url=url_rsc, headers=headers)

    # get server list
    res_srv_select = urllib2.urlopen(req_srv_list)
    json_str_srvlist = res_srv_select.read()
    json_dict_srvlist = json.loads(json_str_srvlist)
    # result check
    rtn_code = int(json_dict_srvlist['result']['code'])
    if rtn_code != 0:
        print('get serverlist abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_srvlist['result']['message']))
        sys.exit()

    #get resource status
    res_rsc_sts = urllib2.urlopen(req_rsc_sts)
    json_str_rscsts = res_rsc_sts.read()
    json_dict_rscsts = json.loads(json_str_rscsts)
    # result check
    rtn_code = int(json_dict_rscsts['result']['code'])
    if rtn_code != 0:
        print('get resource status abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_rscsts['result']['message']))
        sys.exit()

    # print data
    for j in range(len(json_dict_rscsts['resources'])):
	cursrvname = json_dict_rscsts['resources'][j]['current']
	for i in range(len(json_dict_srvlist['servers'])):
	    srvname = json_dict_srvlist['servers'][i]['name']
            if srvname == cursrvname:
                current = json_dict_rscsts['resources'][j]['current']
                print('{0}'.format(current))
                sts = json_dict_rscsts['resources'][j]['status']
                print('{0}'.format(sts))
        if cursrvname == "None":
            current = json_dict_rscsts['resources'][j]['current']
            print('{0}'.format(current))
            sts = json_dict_rscsts['resources'][j]['status']
            print('{0}'.format(sts))

except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()
