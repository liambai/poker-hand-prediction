import sqlite3

# Import Kaggle and CPRG data here:

conn = sqlite3.connect("poker.db")
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "Games";')
c.execute('DROP TABLE IF EXISTS "Hands";')
c.execute('DROP TABLE IF EXISTS "Actions";')

# Create tables in the database and add data to it. REMEMBER TO COMMIT
c.execute('''CREATE TABLE Games(game_ID varchar(256) not null, big_blind float, \
    cards varchar(256), pre_flop_pot float, post_flop_pot float, post_turn_pot float, post_river_pot float)''')
c.execute('''CREATE TABLE Hands(game_ID varchar(256) not null, player_ID varchar(256) not null, \
    card_1 varchar(256), card_2 varchar(256), bets float, net_gain float, chips_at_begining float)''')
c.execute('''CREATE TABLE Actions(game_ID varchar(256) not null, player_ID varchar(256) not null, round_k int not null, \
    position int not null, player_chips varchar(256), action_id varchar(256))''')
conn.commit()

# Insert values into respective tables
    # c.execute('''INSERT INTO Games VALUES (?, ?, ?, ?, ?, ?)''', (<Add stuff in here>))
    # c.execute('''INSERT INTO Hands VALUES (?, ?, ?, ?, ?, ?, ?)''', (<Add stuff in here>))
    # c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?, ?)''', (<Add stuff in here>))
    # conn.commit()
