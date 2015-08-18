import random


class MarkovGenerator(object):
    
    def __init__(self, db_cur, seed_1, seed_2, seed_3):
        self.db = db_cur
        self.seed_1 = seed_1
        self.seed_2 = seed_2
        self.seed_3 = seed_3
        self._generated = [self.seed_1, self.seed_2, self.seed_3]

    def generate(self, words = 100):
        for word_count in xrange(words):
            self._generated.append(self._get_next(*self._generated[-3:]))
        return ''.join(self._generated)


    def _get_next(self, seed_1, seed_2, seed_3):
        query = '''SELECT t4_id AS next, count FROM four_grams WHERE
                        t1_id=? AND
                        t2_id=? AND
                        t3_id=?'''
        params = tuple([self._token_to_id(token) for token in (seed_1, seed_2, seed_3)])
        self.db.execute(query, params)
        next_tokens = self.db.fetchall()

        total_count = sum([count for token_id, count in next_tokens])
        r = random.randint(0, total_count - 1)
        current = 0
        for token_id, count in next_tokens:
            if current + count >= r:
                return self._id_to_token(token_id)
            current += count
        return None

    
    def _id_to_token(self, token_id):
        query = 'SELECT token FROM tokens WHERE id=?'
        params = (token_id,)
        token, = self.db.execute(query, params).fetchone()
        return token

    def _token_to_id(self, token):
        query = 'SELECT id FROM tokens WHERE token=?'
        params = (token,)
        token_id, = self.db.execute(query, params).fetchone()
        return token_id


