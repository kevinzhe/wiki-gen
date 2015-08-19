Wikipedia Generator
===================

Flask dev server
----------------
Here's how to spin up a local Flask server for development purposes. You should use a virtualenv to ensure that you're running the required versions of each module, and have a clean working environment.

1. Get Python 2 (from [Python.org](https://www.python.org) or your package manager) and make sure `python` and `pip` are in your PATH.
2. Get virtualenv for Python 2, either through your package manager or `pip`

        pip install virtualenv

3. Create a new virtualenv stored in `wiki-gen/www/venv`. Assuming you're in the project root:

        cd www
        virtualenv venv

4. Turn on the virtualenv and install the requirements

        source venv/bin/activate
        pip install -r requirements.txt

   for Windows:
   
        venv\scripts\activate
        pip install -r requirements.txt

5. Create the seeds logging database:

        cd wiki-gen
        python manage.py initdb

6. Move the four-grams/tokens database to the db directory:

        mv /path/to/big/four/grams/database.db db/wiki-gen.db

5. Start the server

        cd wiki-gen
        python manage.py runserver

Turn on the virtualenv whenever you're working on the app (ie. step 4 without the install). When you're done, you can turn off the virtualenv and return to normal:

        deactivate


Creating the four-gram database
-------------------------------
The app needs a database of four-grams to generate the Markov chains of text. It uses sqlite, since it provides a quick, lightweight, easy-to-use interface, and performs quite well with read-only databases.

Get [Wikiforia](https://github.com/marcusklang/wikiforia), and use it to extract a [Wikipedia XML dump](https://dumps.wikimedia.org/enwiki/). Then delete the opening and closing `<xml>` tags (`hexdump` allows you to overwrite them with whitespace to prevent a complete rewrite of the file). Make sure Python 3 is installed and in your PATH as `python3`. Then, run:

    ./parse_four_grams.py /path/to/xml/dump /path/to/output/db

The script runs very slowly, since random reads/writes on spinning hard drives are very slow, and the script isn't particularly clever about caching. Writing to an in-memory database in a tmpfs helps speed things up considerably, but you're limited to however much RAM you have. Parsing the first ~600,000 articles in the English Wikipedia resulted in a ~9 GB database, with ~450 million four-grams, and ~12 million unique tokens.

The schema for the database is:

#####tokens

Col | Type
--- | ----
id | INTEGER PRIMARY KEY (alias of built-in rowid)
token | TEXT UNIQUE NOT NULL

#####four\_grams WITHOUT ROWID

Col | Type
--- | ----
t1\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id)
t2\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id)
t3\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id)
t4\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id)
count | INTEGER DEFAULT 1 NOT NULL

Since there are a limted number of tokens in any language, the size of the database remains managable as more four grams are inserted.
