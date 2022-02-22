# URB-RS
An user's reviews based recommender system, developed for my university degree thesis.

Before anything, it's recommended to use a virtual environment. You can either use a pre-set virtual environment as
anaconda, or set a new one in the folder where you're going to clone the repo.

## Set the working environment
To set a new virtual environment, install python, if not already, and then run these in the shell/terminal:

`pip install virtualenv`

`virtualenv venv`

### Activate the virtual environment
#### on Linux
`source ./venv/bin/activate`
#### on Windows
`.\venv\Scripts\activate`

### Install the needed modules
`pip install scrapy sqlalchemy pymysql`

### Create the db and the dba
Log in the mysql cli with root user and create the database and the user admin for it:

`CREATE SCHEMA rs_db;`

`CREATE USER 'rsUser'@'localhost' IDENTIFIED BY 'rs_password';`

`GRANT ALL PRIVILEGES ON rs_db.* TO 'rsUser'@'localhost';`

`FLUSH PRIVILEGES;`

## Fetch the reviews
`cd scraping`

`scrapy crawl fetcher`