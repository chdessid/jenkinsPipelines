update articles set sitename = 'observador' where sitename is NULL and urls like '%observador%' ;
update articles set sitename = 'chron' where sitename is NULL and urls like '%chron.com%' ;
update articles set sitename = 'altibbi' where sitename is NULL and urls like '%altibbi%' ;
update articles set sitename = 'francetvinfo' where sitename is NULL and urls like '%francetvinfo%';
update articles set sitename = 'siasat' where sitename is NULL and urls like '%siasat.com%' ;
update articles set sitename = 'r7brazil' where sitename is NULL and urls like '%r7brazil%' ;
update articles set sitename = 'zyadda' where sitename is NULL and urls like '%zyadda.com%' ;
update articles set sitename = 'mosoah' where sitename is NULL and urls like '%mosoah.com%' ;
update articles set sitename = 'elbalad' where sitename is NULL and urls like '%elbalad.com%' ;
update articles set sitename = 'makeuseof' where sitename is NULL and urls like '%makeuseof%' ;
update articles set sitename = 'wikihow' where sitename is NULL and urls like '%wikihow%' ;
update articles set sitename = 'g1globo' where sitename is NULL and urls like '%g1globo%' ;
update articles set sitename = 'how2shout' where sitename is NULL and urls like '%how2shout%' ;
update articles set sitename = 'sqlshack' where sitename is NULL and urls like '%sqlshack.com%' ;


select count (*), sitename from articles group by sitename order by count asc
