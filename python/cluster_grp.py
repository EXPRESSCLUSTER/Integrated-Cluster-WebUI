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

    url_srv_select = '{0}://{1}:{2}/api/v1/servers?select=name'.format(method, host, port) 
    url_grp = '{0}://{1}:{2}/api/v1/groups'.format(method, host, port) 

    interval = '5'

    headers = {}
    headers["authorization"] = "Basic " + (user + ":" + pwd).encode("base64")[:-1]
    req_srv_list = urllib2.Request(url=url_srv_select, headers=headers)
    req_grp_sts = urllib2.Request(url=url_grp, headers=headers)

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

    #get groups status
    res_grp_sts = urllib2.urlopen(req_grp_sts)
    json_str_grpsts = res_grp_sts.read()
    json_dict_grpsts = json.loads(json_str_grpsts)
    # result check
    rtn_code = int(json_dict_grpsts['result']['code'])
    if rtn_code != 0:
        print('get group status abnormal end.')
        print('  ret code : {}'.format(rtn_code))
        print('  message : {}'.format(json_dict_grpsts['result']['message']))
        sys.exit()

    # print data
    for i in range(len(json_dict_grpsts['groups'])):
        cursrvname = json_dict_grpsts['groups'][i]['current']
        if cursrvname == "None":
            cur_lbl = '{:<32}'.format('current')
            current = json_dict_grpsts['groups'][i]['current']
            print('{0}:{1}'.format(cur_lbl, current))
            name = '{:<32}'.format(json_dict_grpsts['groups'][i]['name'])
            sts = json_dict_grpsts['groups'][i]['status']
            print('{0}:{1}'.format(name, sts))
        else:
            for j in range(len(json_dict_srvlist['servers'])):
                srvname = json_dict_srvlist['servers'][j]['name']
                if cursrvname == srvname:
                    cur_lbl = '{:<32}'.format('current')
                    current = json_dict_grpsts['groups'][i]['current']
                    print('{0}:{1}'.format(cur_lbl, current))
                    name = '{:<32}'.format(json_dict_grpsts['groups'][i]['name'])
                    sts = json_dict_grpsts['groups'][i]['status']
                    print('{0}:{1}'.format(name, sts))
                    continue


except:
    traceback.print_exc()
    print('abnormal end.')
    sys.exit()

