import sqlite3, random

DB_FILE = "/Users/joanchirinos/Desktop/CS/StuyHacks2019/IWasSick/data/bois.db"

formats = {
    'My {} ate my {}': (('dog', 'shorts'), ('cat', 'shorts'), ('mom', 'breakfast')),
    'I couldn\'t {} my {}': (('eat', 'breakfast'), ('find', 'project'), ('find', 'the school'), ('find', 'favorite bucket of beans')),
    'I {} my {}': (('peed', 'pants'), ('killed', 'goat'), ('ate', 'hair')),
    'There was a {} in my {}': (('avalanche', 'house'), ('snake', 'boot'), ('party', 'pants'), ('StuyHacks competition', 'apartment')),
    'I really had to {}': (('pee'), ('cry'), ('cry'), ('cry'))
}

def create_db():
    '''
    Creates the db.
    '''
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()                # facilitate db ops

    c.execute("CREATE TABLE IF NOT EXISTS users(email TEXT, password TEXT)")
    c.execute('CREATE TABLE IF NOT EXISTS saved_excuses(email TEXT, excuse TEXT)')

    db.commit()
    db.close()


def register(email, password, password_check):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if password != password_check:
        return False
    c.execute('INSERT INTO users VALUES(?, ?)', (email, password))
    db.commit()
    db.close()
    return True


def login(email, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE email=?', (email,))
    p = c.fetchall()
    print('THIS IS THE PASSWORD IM CHECKING {}'.format(p[0][0]))
    return p[0][0] == password


def getExcuse():
    f = random.choice(list(formats.keys()))
    ex = f.format(*(random.choice(formats[f])))
    print(ex)
    return ex


def getMyExcuses(email):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT excuse FROM saved_excuses WHERE email=?', (email,))
    excuses = c.fetchall()

    print('THESE ARE THE RAW EXCUSES WE\'RE RETURNING: {}'.format(excuses))
    return excuses


def saveExcuse(email, excuse):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO saved_excuses VALUES(?, ?)', (email, excuse))
    db.commit()
    db.close()


if __name__ == '__main__':
    create_db()
    getExcuse()
    getExcuse()
    getExcuse()
    getExcuse()
