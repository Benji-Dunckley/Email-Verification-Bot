import sqlite3 as sql
# Email Verification Bot.db has a table called 'EmailVerify' with columns 'Name', 'Step' and 'Key'.
dbname = 'Email Verification Bot.db'
# Adding the user to the database after they join a server. Also assigns them unique key
def initial_step(name, key):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    for names in db1cur.execute('''SELECT Name FROM EmailVerify''').fetchall():
        if names[0] == name:  # Stops duplicates.
            return False
    db1cur.execute('''INSERT INTO EmailVerify (Name, Step, Key) VALUES (?, ?, ?) ''', (name, 1, key))
    db1con.commit()
    db1con.close()
    return True


# Updating their step when a user successfully completes the previous one.
def update_step(name, step):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    db1cur.execute('''UPDATE EmailVerify SET Step = ? WHERE Name = ? ''', (step,name))
    db1con.commit()
    db1con.close()


# Checking what step the user is on so the bot can respond accordingly.
def get_step(name):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    cs = db1cur.execute('''SELECT Step FROM EmailVerify WHERE Name = ? ''', (name,)).fetchone()
    db1con.close()
    return cs[0]


# Checking to see if the user has input the correct key.
def get_key(name):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    cs = db1cur.execute('''SELECT Key FROM EmailVerify WHERE Name = ? ''', (name,)).fetchone()
    db1con.close()
    return cs[0]

# Clears user is they need to reset.
def clear_user(name):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    db1cur.execute('''DELETE FROM EmailVerify WHERE Name = ? ''', (name,))
    db1con.commit()
    db1con.close()

# Wipes table.
def clear_table():
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    db1cur.execute('''DROP TABLE EmailVerify''')
    db1cur.execute('''CREATE TABLE EmailVerify (Name, Step, Key) ''')
    db1con.commit()
    db1con.close()
def insert_into(name, step):
    db1con = sql.connect(dbname)
    db1cur = db1con.cursor()
    db1cur.execute('''INSERT INTO EmailVerify (Name, Step, Key) VALUES (?, ?, ?) ''', (name, 1, step))
    db1con.commit()
    db1con.close()
