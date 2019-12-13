# Build and deploy Guacamole from source on CentOS 7

## Prepare all the source and build dependency

Download from https://guacamole.apache.org/releases/1.0.0/

Essential pkgs: 

guacamole-server-1.0.0.tar.gz

guacamole-1.0.0.war

guacamole-auth-jdbc-1.0.0.tar.gz

## Install essential packages for building

    # yum install epel-release
    # yum install cairo-devel libjpeg-turbo-devel libjpeg-devel libpng-devel uuid-devel freerdp1.2-devel gcc

### (Optional) For video recording

    # rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
    # rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
    # yum install ffmpeg-devel pango-devel libssh2-devel libtelnet-devel libvncserver-devel pulseaudio-libs-devel openssl-devel libvorbis-devel libwebp-devel
    # tar xf guacamole-server-1.0.0.tar.gz
    # cd /root/guacamole-server-1.0.0
    # ./configure --with-init-dir=/etc/init.d
    # make install

## Enable and start guacamole server

    # systemctl enable guacd
    # systemctl start guacd

## Setup client without database

    # yum install -y tomcat mariadb-server mysql-connector-java
    # systemctl enable tomcat mariadb
    # systemctl start tomcat mariadb
    # mkdir -p /etc/guacamole/{lib,extensions}

Generate the md5 password.

    # printf '%s' "password" | md5sum

(DON'T do this if use MySQL auth) Generate user-mapping file.

    # cat > /etc/guacamole/user-mapping.xml <<EOF
    <user-mapping>
      <authorize 
        username="demo" 
        password="8383339b9c90775ac14693d8e620981f" 
        encoding="md5">
        <connection name="RHEL 7">
          <protocol>ssh</protocol>
          <param name="hostname">10.53.79.18</param>
          <param name="port">22</param>
          <param name="username">gacanepa</param>
        </connection>
        <connection name="Windows 10">
          <protocol>rdp</protocol>
          <param name="hostname">10.53.79.19</param>
          <param name="port">3389</param>
          <param name="security">tls</param>
          <param name="ignore-cert">true</param>
          <param name="enable-printing">true</param>
        </connection>
        <connection name="VNC Host">
          <protocol>vnc</protocol>
          <param name="hostname">10.53.79.21</param>
          <param name="port">5900</param>
        </connection>
      </authorize>
    </user-mapping>
    EOF

Configure guacd.

    cat > /etc/guacamole/guacamole.properties <<EOF
    guacd-hostname: localhost
    guacd-port: 4822
    EOF

Configure log.

    cat > /etc/guacamole/logback.xml <<EOF
    <configuration>

        <!-- Appender for debugging -->
        <appender name="GUAC-DEBUG" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>

        <!-- Log at DEBUG level -->
        <root level="debug">
            <appender-ref ref="GUAC-DEBUG"/>
        </root>

    </configuration>
    EOF

Copy the guacamole client war to the tomcat directory and start tomcat.

    # cp /root/guacamole-1.0.0.war /var/lib/tomcat/webapps/guacamole.war
    # systemctl restart tomcat

## Client with MySQL Auth, to administrate dynamically

Add following content to the properties file.

    cat >> /etc/guacamole/guacamole.properties <<EOF

    mysql-hostname: localhost
    mysql-port: 3306
    mysql-database: guacdb
    mysql-username: guac_user
    mysql-password: password
    EOF

Copy essential libs.

    # tar xf guacamole-auth-jdbc-1.0.0.tar.gz
    # cp /root/guacamole-auth-jdbc-1.0.0/mysql/guacamole-auth-jdbc-mysql-1.0.0.jar /etc/guacamole/extensions/
    # cp /usr/share/java/mysql-connector-java.jar /etc/guacamole/lib/

Create and initialize the database.

    # mysql -u root
        create database guacdb;
        create user 'guac_user'@'localhost' identified by 'password';
        GRANT ALL PRIVILEGES ON guacdb.* TO 'guac_user'@'localhost';
        flush privileges;
 
    # cat /root/guacamole-auth-jdbc-1.0.0/mysql/schema/*.sql | mysql -u root guacdb

## Restart tomcat service

    service guacd restart
    service tomcat restart

## Login via guacadmin

Open http://your_host:8080/guacamole in your browser.

And the default username/password is gaucamin/guacadmin.

## Guacamole Client API

### Get token

Method: POST

URL:

    http://your_host:8080/guacamole/api/tokens

Headers:

    Basic Auth: guacadmin/guacadmin

Response:

    {
    "authToken": "2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459",
    "username": "guacadmin",
    "dataSource": "mysql",
    "availableDataSources": [
        "mysql",
        "mysql-shared"
    ]
    }

### Delete token

Method: DELETE

Headers:

    Content-Type: application/json

URL:

    http://192.168.0.109:8080/guacamole/api/tokens/2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

### Create connection

Method: POST

URL:

    http://192.168.0.108:8080/guacamole/api/session/data/mysql/connections?token=B1FCBA0CE7BE7A348DB21FFB234F36A1852A140DA173B8B6F6D8A043F7087E1F

Headers:

    Content-Type: application/json;charset=UTF-8

Payload(vnc):

    {"parentIdentifier":"ROOT","name":"test_vnc","protocol":"vnc","parameters":{"port":"5900","read-only":"","swap-red-blue":"","cursor":"","color-depth":"","clipboard-encoding":"","dest-port":"","recording-exclude-output":"","recording-exclude-mouse":"","recording-include-keys":"","create-recording-path":"","enable-sftp":"","sftp-port":"","sftp-server-alive-interval":"","enable-audio":"","hostname":"192.168.0.108","password":"password"},"attributes":{"max-connections":"1","max-connections-per-user":"1","weight":"","failover-only":"","guacd-port":"","guacd-encryption":""}}

Payload(ssh):

    {"parentIdentifier":"ROOT","name":"ssh_con","protocol":"ssh","parameters":{"port":"22","read-only":"","swap-red-blue":"","cursor":"","color-depth":"","clipboard-encoding":"","dest-port":"","recording-exclude-output":"","recording-exclude-mouse":"","recording-include-keys":"","create-recording-path":"","enable-sftp":"","sftp-port":"","sftp-server-alive-interval":"","enable-audio":"","font-size":"","server-alive-interval":"","backspace":"","terminal-type":"","create-typescript-path":"","hostname":"192.168.0.109","username":"root","password":"123456","color-scheme":"black-white"},"attributes":{"max-connections":"1","max-connections-per-user":"1","weight":"","failover-only":"","guacd-port":"","guacd-encryption":""}}

Payload(rdp):

    {"parentIdentifier":"ROOT","name":"rdpppp","protocol":"rdp","parameters":{"port":"3389","read-only":"","swap-red-blue":"","cursor":"","color-depth":"","clipboard-encoding":"","dest-port":"","recording-exclude-output":"","recording-exclude-mouse":"","recording-include-keys":"","create-recording-path":"","enable-sftp":"","sftp-port":"","sftp-server-alive-interval":"","enable-audio":"","security":"","disable-auth":"","ignore-cert":"","gateway-port":"","server-layout":"","console":"","width":"","height":"","dpi":"","resize-method":"","console-audio":"","disable-audio":"","enable-audio-input":"","enable-printing":"","enable-drive":"","create-drive-path":"","enable-wallpaper":"true","enable-theming":"","enable-font-smoothing":"","enable-full-window-drag":"","enable-desktop-composition":"","enable-menu-animations":"","disable-bitmap-caching":"","disable-offscreen-caching":"","disable-glyph-caching":"","preconnection-id":"","hostname":"192.168.0.111","username":"administrator","password":"password"},"attributes":{"max-connections":"1","max-connections-per-user":"1","weight":"","failover-only":"","guacd-port":"","guacd-encryption":""}}

### Delete a connection

Method: DELETE

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/connections/2?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    {"parentIdentifier":"ROOT","name":"test_vnc","protocol":"vnc","parameters":{"port":"5900","read-only":"","swap-red-blue":"","cursor":"","color-depth":"","clipboard-encoding":"","dest-port":"","recording-exclude-output":"","recording-exclude-mouse":"","recording-include-keys":"","create-recording-path":"","enable-sftp":"","sftp-port":"","sftp-server-alive-interval":"","enable-audio":"","hostname":"192.168.0.108","password":"password"},"attributes":{"max-connections":"1","max-connections-per-user":"1","weight":"","failover-only":"","guacd-port":"","guacd-encryption":""}}

### Create user

Method: POST

URL:

    http://192.168.0.108:8080/guacamole/api/session/data/mysql/users?token=B1FCBA0CE7BE7A348DB21FFB234F36A1852A140DA173B8B6F6D8A043F7087E1F

Headers:

    Content-Type: application/json;charset=UTF-8

Payload:

    {"username":"new_user","password":"new_user","attributes":{"disabled":"","expired":"","access-window-start":"","access-window-end":"","valid-from":"","valid-until":"","timezone":null}}

### List users

Method: GET

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

    http://192.168.0.109:8080/guacamole/api/session/data/mysql-shared/users?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

### Bind connection with user

Method: PUT

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    {"username":"demo","attributes":{"guac-email-address":null,"guac-organizational-role":null,"guac-full-name":null,"expired":"","timezone":null,"access-window-start":"","guac-organization":null,"access-window-end":"","disabled":"","valid-until":"","valid-from":""}}

Method: PATCH

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo/permissions?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    [{"op":"add","path":"/connectionPermissions/1","value":"READ"}]

Method: PATCH

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo/userGroups?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    []

### Unbind a connection with user

Method: PUT

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    {"username":"demo","attributes":{"guac-email-address":null,"guac-organizational-role":null,"guac-full-name":null,"expired":"","timezone":null,"access-window-start":"","guac-organization":null,"access-window-end":"","disabled":"","valid-until":"","valid-from":""}}

Method: PATCH

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo/permissions?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    [{"op":"remove","path":"/connectionPermissions/1","value":"READ"}]

Method: PATCH

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/users/demo/userGroups?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:

    []

### List all connections

Method: GET

Headers:

    Content-Type: application/json

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/connectionGroups/ROOT/tree?permission=UPDATE&permission=DELETE&token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

### List active connections

Method: GET

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/activeConnections?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

    http://192.168.0.109:8080/guacamole/api/session/data/mysql-shared/activeConnections?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459


Headers:

    Content-Type: application/json

### Kill an active connections

Method: GET

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/activeConnections?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459


Headers:

    Content-Type: application/json

Payload:

    [{"op":"remove","path":"/1f3234fa-5ccc-4e9b-8be2-ea21c7a00c3c"}]


### Create new ssh connection

Method: 

URL:

    http://192.168.0.109:8080/guacamole/api/session/data/mysql/connections?token=2068C1171C6F6677B7DA3895EDF2D7C0043DD181B84730C79392AB596CFCF459

Headers:

    Content-Type: application/json

Payload:


## Now in your browser

http://your_host:8080/guacamole/#/token=FB962B60FA24D9A34A212AA4AFBDB45393CCAD07DD846093BED5E3ECC329F7A0
