import sqlite3
conn = sqlite3.connect('poker.db')
c = conn.cursor()

def main():
    lines = open("kaggle-data/kaggle_file2.txt" ,"r").readlines()
    games = [[]]
    for line in lines:
        games[-1].append(line)
        if line == '\n':
            games.append([])

    # parse game information and insert into Games table
    for game in games:
        game_id = game[1].split(' ')[2]
        stakes = game[1].split(' ')[3]
        big_blind = stakes.split("/")[1]
        cards = [None]*5
        for line in game:
            words = line.split(" ")
            #get info about the 5 cards on the board
            if words[0] == "Board:":
                cards_info = words[1:]
                for i in range(len(cards_info)):
                    cards[i] = cards_info[i].strip("[]")
        
        c.execute('''INSERT INTO Games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', \
                (game_id, big_blind, cards[0], cards[1], cards[2], \
                cards[3], cards[4], None, None, None, None))

    # parse hand information and insert into Hands table
    player_IDs = []
    game_IDs = []
    card_1 = []
    card_2 = []
    bets = []
    net_gain = []
    chip_stack = []
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

    for pid, gid, c1, c2, b, ng, cs in zip(game_IDs, player_IDs, card_1, card_2, bets, net_gain, chip_stack):
        c.execute('''INSERT INTO Hands VALUES (?, ?, ?, ?, ?, ?, ?)''', (pid, gid, c1, c2, b, ng, cs))

    for game in games:
        game_id = game[1].split(' ')[2]
        round_k = 0 #0 pre-flop, 1 post-flop, 2 post-turn, 3 post-river
        pos_in_round = 0 #0 for first action in round, counting up
        for line in game:
            words = line.split(" ")
            if words[0] == "***":
                round_k += 1
                pos_in_round = 0
            if words[0] == "Player":
                player_id = words[1]
                action_word = words[2].strip("\n ")
                if action_word == 'folds':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'f'))
                if action_word == 'calls':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'c'))
                if action_word == 'raises':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'r'))
                if action_word == 'checks':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'k'))
                if action_word == 'bets':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'b'))
                if action_word == 'allin':
                    pos_in_round += 1
                    c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
                (game_id, player_id, round_k, pos_in_round, 'A'))

    conn.commit()
if __name__ == '__main__':
    main()