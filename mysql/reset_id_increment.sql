SET @num := 0;

UPDATE your_table SET id = @num := (@num+1);

ALTER TABLE tableName AUTO_INCREMENT = 1;
