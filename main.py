logger = open("log.txt", "w")

hand = []
turn = 0
player = ""
teammate = 0
trick = []
played = []
bids = [0, 0, 0, 0]
while (line := input()) != "end":
    logger.write(line + "\n")

    if line[:6] == "player":
        player = line[7]
        teammate = int(player) + 2 % 4
        # logger.write(f"player number {player}, teammate {teammate}\n")

    if line[:4] == "hand":
        hand = line[5:].split()
        # logger.write(f"hand: {hand}\n")

    if line[:3] == "bid":
        id = line[4]
        if id == "?":
            print(0)
        else:
            bids[int(id)] = int(line[6:])
            # logger.write(f"bids: {bids}\n")
    
    if line[:4] == "card":
        id = line[5]
        if id == "?":
            print(0)
        elif id == player:
            hand.remove(line[7:9])
            # logger.write(f"hand: {hand}\n")
        else:
            turn = (turn + 1) % 4
            trick.append(line[7:9])
            # logger.write(f"trick: {trick}\n")
            if not turn: #turn == 0
                played.extend(trick)
                trick = []
