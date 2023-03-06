import random

import random

def public_good_game():
    # Initialize the players as contributors or judge
    players = ["player 1", "player 2", "player 3", "player 4", "judge"]
    random.shuffle(players)
    
    # Distribute the shares to the contributors
    shares = [20] * 5
    for i in range(4):
        share = random.randint(0, shares[i])
        shares[i] -= share
        shares[3] += share
    
    # Calculate the total public good
    public_good = sum(shares) * 2
    
    # Calculate the share for each contributor
    shares = [share * 2 for share in shares]
    
    # Print the shares for each player
    for i in range(5):
        print(f"{players[i]}: {shares[i]}")
    
    # Return the shares for each player
    return shares

public_good_game()