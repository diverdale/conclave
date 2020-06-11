# conclave

You will need a working MySQL/MariaDB installation running and an empty db named `conclave`

* Create a working directory
* Create a venv in that directory:
    on mac `virtualenv .venv ` This creates a hidden venv directory
* Activate venv `src .venv/bin/activate`
* Install requirements `pip install -r requirements.txt`
* Run `flask db init` to initialize the database 
* Run `flask db migrate` if migrations directory exists in the repo, delete it.
* Run `flask db upgrade` to create the empty db
* Test by running `python app.py` If no errors, open browser to
`http://localhost:5000/users/register` and fill out registration form
* If that all works, from db cli run `update user set role = 'Admin' where id = 1` This will give you an admin user


You should be good to go with whatever IDE you use.
