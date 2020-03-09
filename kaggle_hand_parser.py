import sqlite3
import re

conn = sqlite3.connect('poker.db')
c = conn.cursor()
 
def main():
    # data information
    player_IDs = []
    game_IDs = []
    card_1 = []
    card_2 = []
    bets = []
    net_gain = []
    chip_stack = []

    # parsing the txt file
    lines = open('kaggle-data/kaggle_file1.txt', 'r').readlines()
    games = [[]]
    for line in lines:
        games[-1].append(line)
        if line == '\n':
            games.append([])

    for game in games:
        game_length = len(game)
        for line in game:
            words = line.split(' ')
            if words[0] == 'Seat' and len(words[1]) == 2:
                # get info on player_id
                player_IDs.append(' '.join(words[2:-1]))
                # get info on game_id
                game_IDs.append(game[1].split(' ')[2])
                # get info on chip stack
                chip_stack.append(float(words[-1].strip('().\n')))
            # iterate through summary
            if line == '------ Summary ------\n':
                summary_index = game.index(line)
                for i in range(summary_index, game_length):
                    summary_words = game[i].split(' ')
                    summary_line_length = len(summary_words)
                    if summary_words[0] == 'Player' or summary_words[0] == '*Player':
                        if summary_words[2] == 'shows:':
                            for word in summary_words:
                                # get info on first card
                                if word.startswith('['):
                                    card_1.append(word.strip('['))
                                # get info on second card
                                if word.endswith('].'):
                                    card_2.append(word.strip('].'))
                        else:
                            # otherwise there was no show
                            card_1.append(None)
                            card_2.append(None)
                    for j in range(summary_line_length):
                        if summary_words[j].endswith('Bets:'):
                            # get info on bet
                            bet_index = summary_words.index(summary_words[j]) + 1
                            bet = float(summary_words[bet_index].strip('.'))
                            bets.append(bet)
                            # get info on net gain
                            collects_index = bet_index + 2
                            collect = float(summary_words[collects_index].strip('.'))
                            net_gain.append(collect - bet)

    # Create connection to database
    conn = sqlite3.connect('poker.db')
    c = conn.cursor()

    # Delete table if exists
    c.execute('DROP TABLE IF EXISTS "Hands";')

    # Create table in the database
    c.execute('''CREATE TABLE Hands(
    game_ID varchar(256) not null, 
    player_ID varchar(256) not null, 
    card_1 varchar(256), 
    card_2 varchar(256), 
    bets float, 
    net_gain float, 
    chips_at_begining float, 
    PRIMARY KEY(player_ID, game_ID))''')

    for gid, pid, c1, c2, b, ng, cs in zip(player_IDs, game_IDs, card_1, card_2, bets, net_gain, chip_stack):
        c.execute('''INSERT INTO Hands VALUES (?, ?, ?, ?, ?, ?, ?)''', (gid, pid, c1, c2, b, ng, cs))

    conn.commit()



if __name__ == '__main__':
    main()