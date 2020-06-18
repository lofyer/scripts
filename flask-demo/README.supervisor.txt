1. Install supervisor
apt install supervisor

2. Edit /etc/supervisor/conf.d/dingding_robot.conf
[program:dingding_robot]
command=python3 main.py
directory=/root/zstack-dingding-robot
user=root
autostart=true
stopasgroup=true
killasgroup = true
startsecs = 5
autorestart=true
redirect_stderr=true
stdout_logfile=/root/zstack-dingding-robot/worker.log

3. Edit /etc/supervisor/supervisord.conf
[inet_http_server]
port=*:9001
username=root
password=pswd4root
