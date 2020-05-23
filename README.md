Initially this[https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc] guide was followed for setup.


This app uses flask_sqlalchemy to define the infection model, psycopg to interact with it and flask to build the interface, bootstrap as the theme


source env/bin/activate to go into virtenv
dashboard theme from https://themewagon.com/themes/open-source-bootstrap-admin-template/

progress:

![0](progress/0.png)
![1](progress/1.png)




heroku pg:psql --app YOUR_APP_NAME_HERE < updates.sql
pg_dump dbname > outfile



The site works well however since the current data has over 370k lines, all of which are imported into the database, this breaks the 10k row data cap. Creating precomputed aggregated tables for each state and the US as a whole while limit the rows to only around 6.7k. This will leave a couple months worth more rows which could be added to the database instance. This will require a rewrite of some of the code.


https://www.worldometers.info/coronavirus/country/us/