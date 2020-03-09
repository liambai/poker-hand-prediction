import sqlite3
conn = sqlite3.connect('poker.db')
c = conn.cursor()

def main():
    lines = open("kaggle-data/kaggle_file1.txt" ,"r").readlines()
    games = [[]]
    for line in lines:
        games[-1].append(line)
        if line == '\n':
            games.append([])
    
    for game in games:
        game_id = game[1].split(' ')[2]
        stakes = game[1].split(' ')[3]
        for line in game:
            words = line.split(" ")
            
            #get info about the 5 cards on the board
            if words[0] == "Board:":
                cards = [None]*5
                cards_info = words[1:]
                for i in range(len(cards_info)):
                    cards[i] = cards_info[i].strip("[]")
                
        
        c.execute('''INSERT INTO Games VALUES (?, ?, ?, ?, ?, ?, ?)''', (game_id, stakes, None, None, None, None, None))
        conn.commit()
if __name__ == '__main__':
    main()