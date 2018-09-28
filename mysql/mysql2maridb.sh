mysqld_safe --skip-grant-tables &

mysql

UPDATE mysql.user SET authentication_string = PASSWORD('mypassword'), plugin = 'mysql_native_password' WHERE User = 'root' AND Host = 'localhost';

exit
