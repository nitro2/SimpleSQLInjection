# SimpleSQLInjection
Demo SQL injection attack on a localhost Flask Web server

# Setup
## Install dependencies
> `python3 -m pip install -r requirements.txt`

## Run Web server
> `python3 app.py

## Default login
Open your web browser at: http://localhost:5000
[docs/login.png](docs/login.png)

Type username/password: `a/b`

If you enter correct password, you will login to index page:

[docs/index.png](docs/index.png)


# SQL Injection Attack
In Login page, enter: `' OR '1'='1';--` into username field then login
You will bypass the login page

Enjoy!



