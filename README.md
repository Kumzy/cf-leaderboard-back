# cf-leaderboard-back

## Installation

### Create database and extensions
```sql
create database cf_leaderboard;
create extension if not exists "pgcrypto";
```

### Initialise the database
```
flask db init
flask db upgrade
```


## Udpate the db after a modification
```
flask db migrate -m "<comment>"
flask db upgrade
```

## Run
```
uwsgi --socket 0.0.0.0:5000 --protocol=http -w cf_leaderboard:app
```