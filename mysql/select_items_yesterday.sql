select id,title,content,url,date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d') as date_new from posts where date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d')=curdate()+0-1;

OR

select id,content_hash,title,content,url,date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d') as date_new from posts where date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d')=subdate(current_date, 1) group by title;
