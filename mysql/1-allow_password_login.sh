mysqld_safe --skip-grant-tables &
mysql -uroot
> use mysql;
> UPDATE user SET plugin="";
