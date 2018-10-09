mysqld_safe --skip-grant-tables &
use mysql;
UPDATE user SET plugin="";
