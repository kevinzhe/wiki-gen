Wikipedia Generator
===================

Creating the four-gram database
-------------------------------
The app needs a database of four-grams to generate the Markov chains of text. It uses sqlite, since it provides a quick, lightweight, easy-to-use interface, and performs quite well with read-only databases.

Get [Wikiforia](https://github.com/marcusklang/wikiforia), and use it to extract a [Wikipedia XML dump](https://dumps.wikimedia.org/enwiki/). Then delete the opening and closing `<xml>` tags (`hexdump` allows you to overwrite them with whitespace to prevent a complete rewrite of the file). Make sure Python 3 is installed and in your PATH as `python3`. Then, run:

    ./parse_four_grams.py /path/to/xml/dump /path/to/output/db

The script runs very slowly, since random reads/writes on spinning hard drives are very slow, and the script isn't particularly clever about caching. Writing to an in-memory database in a tmpfs helps speed things up considerably, but you're limited to however much RAM you have. Parsing the first ~600,000 articles in the English Wikipedia resulted in a ~9 GB database, with ~450 million four-grams, and ~12 million unique tokens.

The schema for the database is:

tokens
| Col | Type |
| :-: | :-: |
| id | INTEGER PRIMARY KEY (alias of built-in rowid) |
| token | TEXT UNIQUE NOT NULL |

four\_grams WITHOUT ROWID
| Col | Type |
| :-: | :-: |
| t1\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id) |
| t2\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id) |
| t3\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id) |
| t4\_id | INTEGER NOT NULL PRIMARY KEY FOREIGN KEY REFERENCES token(id) |
| count | INTEGER DEFAULT 1 NOT NULL |

Since there are a limted number of tokens in any language, the size of the database remains managable as more four grams are inserted.
