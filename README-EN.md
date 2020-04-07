# Integrated Cluster WebUI by RESTful API

### About this guide
We have released EXPRESSCLUSTER X 4.2 .
We have started offering API services to enhance cooperation with other products.(RESTful API as below)

To begin with, RESTful API service is running as HTTP Server on each server in the cluster.
Users or applications that is running on a client machine can send HTTP / HTTPS requests to RESTful API service to get various cluster status and operate the cluster.
Once RESTful API service receives HTTP / HTTPS requests from them, it returns the processed result as HTTP response.

By using this function, you will be able to unify the management of EXPRESSCLUSTER cluster systems. (Integrated Cluster WebUI as below) 
 
As sample, we provide Integrated Cluster WebUI's script.
In the following section, this document describes how to use the sample script. 

### Configuration
```
 |
 |  +-----------------------------------+
 +--| EXPRESSCLUSTER X 4.2 for Windows  |
 |  | - 2node cluster		                +-----------+
 |  +-----------------------------------+	          |
 |						    |                                 |
 |  +--------------------------------+              |
 +--| EXPRESSCLUSTER X 4.2 for Linux |    +---------+---------+       +--------------+
 |  | - 3node cluster                +----+                   |       |              |
 |  +--------------------------------+    | Integrated        |       |              |
 |                                        | Cluster WebUI     +-------+    Client    |
 |  +--------------------------------+    | Server            |       |              |
 +--| EXPRESSCLUSTER X 4.2 for Linux +----+                   |       |              |
 |  | - 2node cluster                |    +-------------------+       +--------------+
 |  +--------------------------------+
```


### Precondition
- EXPRESSCLUSTER X 4.2 (internal version 4.2.0-1 / 12.20 ～)
- need to install node.js for EXPRESSCLUSTER Server

### Setup EXPRESSCLUSTER X
Turn on the setting Cluster Properties > API tab > Enable API Service  
After select Communication Method(http or https), push the Apply the Configuration server.  
Default port number is 29009.  
If you want to edit port number, you have to edit Cluster Properties > Port No. > API HTTP Port Number.  

### How to use sample script
1. Install php and Apache for Integrated Cluster WebUI Server.    
2. Download the ecxinfo-1.0.0.tar.gz anywhere.  
3. Extract the ecxinfo-1.0.0.tar.gz  to /var/www/html.   
   - #cd /var/www/html  
   - #tar -zxvf ecxinfo-1.0.0.tar.gz  
4. set cluster information to /www/var/html/config.ini.  
  - For example,
 
    | Parameters | Explanation |
    | ---- | ---- |
    | [1] | Section number |
    | method = http | select http or https |
    | user = test_user | set username to executing RESTFul API |
    | pwd = test_pwd | set password to executing RESTFul API |
    | host = 192.168.0.1 | set ipaddress to executing RESTFul API |
    | port = 29009 | set port number to executing RESTFul API |

5. enter the web browser  
    - http://IPaddress/ecxinfo.php
    	- IPaddress is Integrated Cluster WebUI Server's IPaddress.

### Notes
- For the section number specified in config.ini, make sure to specify a serial number starting from 1.
- It is necessary to set a serial number starting from 1 editing config.ini.
- If the parameters described in config.ini are incomplete, Integrated Cluster WebUI may not be displayed correctly.
- For the IP address specified in config.ini, specify only one of the IP addresses belonging to the cluster.
- If a cluster have multiple failover groups, you cannot get what group resources belong to.

### Directory structure
```
ecx_information.tar.gz
    |
    |- ecxinfo.php
    |- config.ini
    |- python
    |    |- cluster_cls.py
    |    |- cluster_grp.py
    |    |- cluster_mon.py
    |    |- cluster_rsc.py
    |    |- cluster_srv.py
    |
    |- image
         |- kurara.png
```

### Software / OS versions

- Integrated Cluster WebUI Server
    - Red Hat Enterprise Linux Server release 7.6 (Maipo)

- Apatch
```
Server version: Apache/2.4.6 (Red Hat Enterprise Linux)
Server built:   Jun 22 2018 01:19:25
```
- php
```
PHP 5.4.16 (cli) (built: Jun 19 2018 13:09:01)
Copyright (c) 1997-2013 The PHP Group
Zend Engine v2.4.0, Copyright (c) 1998-2013 Zend Technologies
```
- node.js 
    - v10.16.3
