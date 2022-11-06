# Spending Tracker

This is a spending tracker created as a project submission for the Python as part of the Professional Software Development Award at CodeClan.

## Setup

Clone the repo with:

```bash
git clone https://github.com/inkyblinkypinkyclyde/spending_tracker_again
```

If you would like the app to send reminder emails for payments add an email credentials file to the main directory.

The file should look something like this:

```bash
# name emailcredentials.py
email = "your gmail account"
password = "your password"
```



Create a postgres database...

```bash
createdb spending_tracker
```

...and connect it to the provided schema by running the following command from within the project's main directory:

```bash
psql -d spending_tracker -f db/spending_tracker.sql
```


You can now run the app:
```bash
python app.py
```

You can add sample data by running:
```bash
python console.py
```

and the app can be viewed on at http://127.0.0.1:5000/


## Technologies used
* Python (v3.9.12)
* PostgreSQL (v14.5)
* Flask (v2.1.2)
* Flask-Mail (v0.9.1)
* Jinja2 (v3.1.2)
* Psycopg2 (v2.9.3)
 

## Future updates
* Add the option to send calendar reminders for future payments
* Refactor the backend logic for calculating totals
* refine email notifications