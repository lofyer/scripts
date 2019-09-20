1. Change conf /etc/mysql/mariadb.conf.d/50-server.conf
[server]
skip-networking = 0
bind-address = 0.0.0.0

2. Run
mysql_secure_installation
