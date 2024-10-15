from motion import movement
from postions_played import positions_played

# Main game loop
def play_game():
    game = TicTacToe()  # Initialize the game board
    agent_type = choose_agent()  # Ask user to choose the agent

    if agent_type == "minimax":
        agent = MinimaxAgent(game)  # Use Minimax agent
    else:
        agent = RandomAgent(game)  # Use Random agent

    global player_positions_stored
    player_positions_stored=[]    # storing the positions which player has played
    global robot_positions_stored
    robot_positions_stored=[]     # storing positions which robot has played
    global pick_up_list
    pick_up_list=['c1','c2','c3','c4','c5','c6,''c7','c8','c9','c10']
    global pickup_index
    pickup_index = 0

    # Game loop
    while True:
        
        # Player X's turn (user)
        players_input=positions_played()


        if len(players_input) > 0:
            position_input = players_input[-1]
        print('only',position_input)
        

        position = int(position_input[1]) - 1 
        print('only',position)
        #print(int(position_input[1]) - 1 )
         # Convert to 0-based index
        if not game.make_move(position, "X"):  # If the move is invalid
            print("Invalid move! Try again.")
            continue
        player_positions_stored.append(position)
        
        if game.is_winner("X"):
            print("You win!")
            break
        elif len(game.available_moves()) == 0:
            print("It's a tie!")
            break

        # Agent's turn (O)

        
        agent_move = agent.get_move()  # Get the move from the agent

        movement(agent_move+1,pickup_index=pickup_index)

        game.make_move(agent_move, "O") # Agent makes its move
        print(f"Agent plays at position: p{agent_move+1}")
        robot_positions_stored.append(f'p{agent_move+1}')
        pickup_index+=1


        if game.is_winner("O"):
            print("Agent wins!")
            break
        elif len(game.available_moves()) == 0:
            print("It's a tie!")
            break
    print(player_positions_stored)
    print(robot_positions_stored)


# Start the game
play_game()
from clear_field import clear_space

movement(robot_positions_stored,player_positions_stored,clear_out=True)

