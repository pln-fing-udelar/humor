# HUMOR corpus

Repository containing scripts and data related to the HUMOR corpus.

## Load the v1 corpus in MySQL

1. Install MySQL
2. Create a database.
3. Run:

```shell
mysql -u $USER -p $DATABASE < corpus.sql
```

## Scripts setup

Install [pipenv](https://docs.pipenv.org/). Then:

```
pipenv install
pipenv shell
```
