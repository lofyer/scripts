1. join whole table
select * from posts inner join rss_rating on posts.content_hash=rss_rating.content_hash where rss_rating.country="China";

2. join one or more column

2 tables
select posts.*,rss_rating.country from posts inner join rss_rating on posts.content_hash=rss_rating.content_hash where rss_rating.country="China" limit 1;

3 tables
select posts.*,rss_rating.country,city_map.country_iso,city_map.continent,city_map.country_currency,city_map.country_currency_iso from posts inner join rss_rating on posts.content_hash=rss_rating.content_hash inner join city_map on rss_rating.country=city_map.country where rss_rating.country="Canada";

3. single table
select * from posts where posts.content_hash in (select content_hash from rss_rating  where country="China");

