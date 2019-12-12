# Build and deploy Guacamole from source on CentOS 7

## Prepare all the source and build dependency

Download from https://guacamole.apache.org/releases/1.0.0/

Essential pkgs: 

guacamole-server-1.0.0.tar.gz

guacamole-1.0.0.war

guacamole-auth-jdbc-1.0.0.tar.gz

## Install essential packages for building

    # yum install cairo-devel libjpeg-turbo-devel libjpeg-devel libpng-devel uuid-devel freerdp1.2-devel

### (Optional) For video recording

    # yum install epel-release
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
    # systemctl enable tomcat
    # systemctl start tomcat

## Client with MySQL Auth, to administrate dynamically

Add following content to the properties file.

    cat >> /etc/guacamole/guacamole.properties <<EOF
    mysql-hostname: localhost
    mysql-port: 3306
    mysql-database: guacdb
    mysql-username: guac_user
    mysql-password: somesecret
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