# Casita

Casita is an unfinished aggregator for real-estate. It scraped data from OLX and Custo Justo, using Scrapy, and this data was then shown in a Django app.

SETUP
-----

1. Upload location data to the database:

    copy locations (distrito, concelho, freguesia)
    from 'freguesias-metadata.csv'
    with (format csv, header true);

    insert into locations (distrito, concelho, freguesia)
    select distinct distrito, concelho, null from locations;

select *, similarity(freguesia, '<FREGUESIA>') as sml
from locations
where freguesia is not null
order by sml desc
limit 1;

AUTHORS
-------

Copyright © 2020 Vitor Manuel de Sousa Pereira. Todos os direitos reservados.
