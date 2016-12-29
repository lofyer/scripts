create table TB(
id int(11) NOT NULL AUTO_INCREMENT,
name varchar(128) DEFAULT NULL,
hash varchar(128) DEFAULT NULL,
PRIMARY KEY (id),
KEY hash_index (hash)
)DEFAULT CHARSET=utf8;;
