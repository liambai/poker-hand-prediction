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
                conn.commit()
            if action_word == 'calls':
                pos_in_round += 1
                c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
              (game_id, player_id, round_k, pos_in_round, 'c'))
                conn.commit()
            if action_word == 'raises':
                pos_in_round += 1
                c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
              (game_id, player_id, round_k, pos_in_round, 'r'))
                conn.commit()
            if action_word == 'checks':
                pos_in_round += 1
                c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
              (game_id, player_id, round_k, pos_in_round, 'k'))
                conn.commit()
            if action_word == 'bets':
                pos_in_round += 1
                c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
              (game_id, player_id, round_k, pos_in_round, 'b'))
                conn.commit()
            if action_word == 'allin':
                pos_in_round += 1
                c.execute('''INSERT INTO Actions VALUES (?, ?, ?, ?, ?)''', \
              (game_id, player_id, round_k, pos_in_round, 'A'))
                conn.commit()