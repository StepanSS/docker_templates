## Flask with SQL Alchemy 

### Contains:

- SQL-Alchemy basic tables: 1-to-many, many-to-many

- cli commands for

- docker-compose files:
> docker-compose.yml - build entire project with docker 
> docker-compose.local.yml - local developing 

#### Build and run entire project with docker
```
# build PostgreSQL db
docker-compose -f docker-compose.yml
```

#### Developing
```
# install project dependencies 
cd web
mkdir .venv
pipenv shell
pipenv install

cd ..

# build PostgreSQL db
docker-compose -f docker-compose.local.yml

# run flask dev server
python web/manage.py run
```

##### check cli commands in web/manage.py
```
# create db
python web/manage.py create_db 

# add data to one_to_many tables
python web/manage.py one_to_many 

# add data to many_to_many tables
python web/manage.py many_to_many 

# del parent row from one_to_many tables
python web/manage.py del_one 

# del row from Product tables (many_to_many)
python web/manage.py del_left_fm_many 

# del row from User tables (many_to_many)
python web/manage.py del_right_fm_many 

```

