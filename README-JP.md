# RESTful API を使用した統合Cluster WebUI

### はじめに
CLUSTERPRO X 4.2 では、他製品との連携強化を目的として APIサービス(以降、RESTful API)の提供を開始しました。  

RESTful APIとは、クラスタ内の各サーバ上でHTTPサーバを起動し、クラスタ外の各クライアント上で実行された
アプリケーションから送信された各種ステータス情報取得要求、各種クラスタ関連操作要求を
HTTP/HTTPSリクエストとして受信し、処理結果をHTTPレスポンスで返却します。

本機能を使用することで、CLUSTERPROを導入している複数のクラスタの状態を一元的に管理(以降 統合Cluster WebUI)すること が可能となります。

サンプルとして、phpファイルを使用した、統合 Cluster WebUI 用スクリプトを作成しましたので、提供いたします。  
これ以降、本ドキュメントでは、サンプルスクリプトの使用方法について記載していきます。

### 構成
```
 |
 |  +---------------------------------+
 +--| CLUSTERPRO X 4.2 for Windows    |
 |  | - 2node cluster		      +-------------+
 |  +---------------------------------+		    |
 |						    |
 |  +----------------------------+                  |
 +--| CLUSTERPRO X 4.2 for Linux |        +---------+---------+       +--------------+
 |  | - 3node cluster            +--------+                   |       |              |
 |  +----------------------------+        | 統合CLUSTER       |       |              |
 |                                        |  WebUI Server     +-------+ クライアント |
 |  +----------------------------+        |                   |       |              |
 +--| CLUSTERPRO X 4.2 for Linux +--------+                   |       |              |
 |  | - 2node cluster            |        +-------------------+       +--------------+
 |  +----------------------------+
```


### 前提条件
CLUSTERPRO X 4.2 (内部バージョン 4.2.0-1 / 12.20 ～)  
CLUSTERPROをインストールしている各サーバに node.js をインストールする  

### CLUSTERPROの設定
クラスタプロパティ > APIタブ > APIサービスを有効にする を ON  
使用したい通信方式(http or https)を選択後、OK を押下し、設定の反映を行う。  
デフォルトのポート番号は 29009 を使用しています。  
修正したい場合は クラスタプロパティ > ポート番号 > API HTTPポート番号 を変更してください。

### サンプルスクリプトの使い方
1. 統合Cluster WebUI 用サーバに php / Apache をインストールする  
2. サンプルスクリプト等を以下の構成で配置する  
```
var/
　└ www/
　   └ html/
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
3. /www/var/html/config.ini に追加したいクラスタの情報を記載する。  
  - 追記内容は以下です
 
    | パラメータ | 説明 |
    | ---- | ---- |
    | [1] | セクション数 |
    | method = http | http or https を記載 |
    | user = test_user | RESTFul API を実行する ユーザ名 を記載 |
    | pwd = test_pwd | RESTFul API を実行する パスワード を記載 |
    | host = 192.168.0.1 | RESTFul API を実行する IPアドレス を記載 |
    | port = 29009 | RESTFul API で使用する ポート番号 を記載 |

4. webブラウザにて以下を実施してください  
    - http://IPaddress/ecxinfo.php

### 注意事項
・config.iniに指定するセクションは 必ず1からの連番 を指定してください。  
・config.iniに記載したパラメータに不備がある場合は、正しく表示されない場合があります。  
・config.iniに指定するIPアドレスは、クラスタに所属するIPアドレスのうち、１つのみの指定ください。  
・グループが複数存在するクラスタの場合、グループに存在するリソースが正しく取得できません。次期バージョン以降対応いたします。  

### 補足情報
- 統合Cluster WebUI 用サーバ
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
