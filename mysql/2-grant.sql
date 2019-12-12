ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
grant all privileges on *.* to root@'%' identified by '123456';
flush privileges;
