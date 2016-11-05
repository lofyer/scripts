delete from posts where id not in (select * from (select max(n.id) from posts n group by n.title) x);

OR

create table new as select * from posts where 1 group by url;
rename table new master;
