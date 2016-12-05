SET @num := 0;
UPDATE your_table SET id = @num := (@num+1);

# or

# ALTER TABLE tableName AUTO_INCREMENT = 1;

then

alter table posts add primary key (id);
alter table posts modify column id int auto_increment;
