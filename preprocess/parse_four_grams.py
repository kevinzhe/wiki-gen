#!/usr/bin/env python3

'''
Parse four-grams from a corpus generated by Wikiforia into a sqlite3 database.
'''


import os
import sqlite3
import string
import sys
import time

CACHE_ARTICLES = 1000

def log(msg):
    print(msg, file = sys.stderr)
    sys.stderr.flush()

def create_tables(conn, cur):
    '''Create four-gram and word id tables in database'''
    words = '''\
CREATE TABLE tokens (
    id INTEGER PRIMARY KEY,
    token TEXT UNIQUE NOT NULL
)'''
    four_grams = '''\
CREATE TABLE four_grams (
    t1_id INTEGER NOT NULL,
    t2_id INTEGER NOT NULL,
    t3_id INTEGER NOT NULL,
    t4_id INTEGER NOT NULL,
    count INTEGER DEFAULT 1 NOT NULL,
    PRIMARY KEY (t1_id, t2_id, t3_id, t4_id),
    FOREIGN KEY (t1_id) REFERENCES token (id),
    FOREIGN KEY (t2_id) REFERENCES token (id),
    FOREIGN KEY (t3_id) REFERENCES token (id),
    FOREIGN KEY (t4_id) REFERENCES token (id)
) WITHOUT ROWID'''
    cur.execute(words)
    conn.commit()
    cur.execute(four_grams)
    conn.commit()

def get_token_ids(tokens, cur):
    '''Return a list of token ids corresponding to the list of tokens'''
    select = 'SELECT id FROM tokens WHERE token=?'
    insert = 'INSERT INTO tokens (token) VALUES (?)'
    ids = [cur.execute(select, (token,)).fetchone()[0] for token in tokens]
    for idx, t_id in enumerate(ids):
        if t_id is not None:
            continue
        cur.execute(insert, (tokens[idx],))
        t_id = cur.lastrowid
        ids[idx] = t_id
    return ids

def get_token_id(token, cur):
    '''Return the id for a token'''
    select = 'SELECT id FROM tokens WHERE token=?'
    t_id = cur.execute(select, (token,)).fetchone()
    if t_id is None:
        insert = 'INSERT INTO tokens (token) VALUES (?)'
        t_id = cur.execute(insert, (token,)).lastrowid
    else:
        (t_id,) = t_id
    return t_id

ids_cache = {}
def insert_grams(counter, cur):
    '''Insert the four-grams in counter into the db'''
    # Prepare the queries
    select = '''SELECT count FROM four_grams WHERE
                    t1_id=? AND
                    t2_id=? AND
                    t3_id=? AND
                    t4_id=?'''
    update = '''UPDATE four_grams SET count=? WHERE
                    t1_id=? AND
                    t2_id=? AND
                    t3_id=? AND
                    t4_id=?'''
    insert = 'INSERT INTO four_grams (t1_id, t2_id, t3_id, t4_id, count) VALUES (?,?,?,?,?)'
    for gram, count in counter.items():
        # First build a tuple of token ids from the gram
        gram_ids = []
        global ids_cache
        for token in gram:
            if token not in ids_cache:
                ids_cache[token] = get_token_id(token, cur)
            gram_ids.append(ids_cache[token])
        gram_ids = tuple(gram_ids)
        # Get the existing count
        existing_count = cur.execute(select, gram_ids).fetchone()
        if existing_count is None:   # Not in db yet
            cur.execute(insert, gram_ids + (count,))
        else:                        # Update existing record
            (existing_count,) = existing_count
            cur.execute(update, (existing_count+count,) + gram_ids)

def get_db(db_path):
    '''Get a connection and cursor to the db'''
    conn = sqlite3.connect(db_path)
    # Foreign key enforcement seems to cause issues with inserting into four_grams
    #conn.execute('pragma foreign_keys=on')
    cur = conn.cursor()
    return conn, cur


def tokenize(segment):
    '''Turn an arbitrary string into a list of tokens'''
    i = 0
    tokens = []
    current = []
    while i < len(segment):
        c = segment[i]
        if c in string.whitespace:
            current.append(c)
            token = ''.join(current)
            if not token.isspace():
                tokens.append(token)
            current = []
            i += 1
        elif c == '[':
            if i+1 < len(segment) and segment[i+1] != '[':
                current.append(c)
                i += 1
                continue
            if len(current) > 0:
                current.append(' ')
                token = ''.join(current)
                if not token.isspace():
                    tokens.append(token)
                current = []
            while i < len(segment) and segment[i] != ']':
                i += 1
            i += 1
            if i < len(segment) and segment[i] == ']':
                i += 1
            while i < len(segment) and segment[i] in string.whitespace:
                i += 1
        elif c == '<':
            if not ((i+4 < len(segment) and segment[i+1:i+5] == 'page') or
                    (i+5 < len(segment) and segment[i+1:i+6] == '/page')):
                current.append(c)
                i += 1
                continue
            if len(current) > 0:
                current.append(' ')
                token = ''.join(current)
                if not token.isspace():
                    tokens.append(token)
                current = []
            while i < len(segment) and segment[i] != '>':
                i += 1
            i += 1
            while i < len(segment) and segment[i] in string.whitespace:
                i += 1
        else:
            current.append(c)
            i += 1
    if len(current) > 0:
        tokens.append(''.join(current))
    return tokens

def count_tokens_grams(tokens):
    counter = {}
    for i in range(len(tokens)-3):
        t1 = tokens[i]
        t2 = tokens[i+1]
        t3 = tokens[i+2]
        t4 = tokens[i+3]
        key = (t1, t2, t3, t4)
        if key in counter:
            counter[key] += 1
        else:
            counter[key] = 1
    return counter


def parse_xml(xml_path, db_path):
    '''Parse the xml into a new database'''
    conn, cur = get_db(db_path)
    log('Creating tables...')
    create_tables(conn, cur)
    with open(xml_path) as corpus:
        lines_cache = []
        articles_count = 0
        start_time = time.time()
        last_time = start_time
        total_articles = 0
        for line in corpus:
            if line.lstrip().startswith('<page'):
                articles_count += 1
            lines_cache.append(line)
            if articles_count >= CACHE_ARTICLES:
                tokens = tokenize(''.join(lines_cache))
                lines_cache = []
                counter = count_tokens_grams(tokens)
                try:
                    insert_grams(counter, cur)
                    conn.commit()
                except:
                    log('ERROR: Insert error')
                total_articles += articles_count
                log('{articles} inserted in {sec} sec'.format(
                        articles = total_articles,
                        sec = time.time() - last_time))
                articles_count = 0
                last_time = time.time()
    log('================================')
    log('committing...')
    conn.commit()
    log('closing connection...')
    conn.close()
    log('{articles} inserted in {sec} sec'.format(
            articles = total_articles,
            sec = time.time() - start_time))

def main():
    if len(sys.argv) != 3:
        log('Usage: {name} [parsed_xml] [out_db]'.format(name = sys.argv[0]))
        sys.exit(1)
    xml_path = sys.argv[1]
    db_path = sys.argv[2]
    if not os.path.isfile(xml_path):
        log('Could not find {path}'.format(path = xml_path))
        sys.exit(1)
    if os.path.isfile(db_path):
        log('{path} already exists'.format(path = db_path))
        sys.exit(1)
    parse_xml(xml_path, db_path)
    sys.exit(0)

if __name__ == '__main__':
    main()
