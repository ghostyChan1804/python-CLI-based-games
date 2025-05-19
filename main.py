import random

class SnakesLadders:
    """
    Advanced Snakes and Ladders game featuring AI learning, dynamic difficulty, and **randomly placed snakes/ladders**.
    """

    def __init__(self, size=100, difficulty="normal", num_snakes=10, num_ladders=10):
        """Initializes a randomized board, AI learning system, difficulty settings, player positions, and turn control."""
        self.size = size
        self.snakes = self.generate_snakes(num_snakes)
        self.ladders = self.generate_ladders(num_ladders)
        self.power_ups = {10: "teleport", 30: "extra_roll", 55: "snake_immunity"}
        self.ai_memory = {}  # Tracks risky spots for AI learning
        self.difficulty = difficulty
        self.player_position = 1
        self.ai_position = 1
        self.turn = "player"

    def generate_snakes(self, num_snakes):
        """Randomly generates snake positions where each snake moves down."""
        snakes = {}
        for _ in range(num_snakes):
            start = random.randint(10, self.size - 10)
            end = random.randint(1, start - 5)  # Ensure snakes always move downward
            snakes[start] = end
        return snakes

    def generate_ladders(self, num_ladders):
        """Randomly generates ladder positions where each ladder moves up."""
        ladders = {}
        for _ in range(num_ladders):
            start = random.randint(1, self.size - 10)
            end = random.randint(start + 5, min(self.size, start + 20))  # Ensure ladders move upward
            ladders[start] = end
        return ladders

    def roll_dice(self):
        """Simulates rolling a dice."""
        return random.randint(1, 6)

    def move(self, position, player_type):
        """Handles movement, snake/ladder encounters, AI learning, and power-ups."""
        dice_roll = self.roll_dice()

        if player_type == "ai" and self.difficulty == "hard":
            dice_roll = self.ai_strategy(dice_roll)

        new_position = position + dice_roll

        if new_position > self.size:
            return position  # Prevent moving beyond final position

        if new_position in self.snakes:
            if player_type == "ai" and "snake_immunity" in self.ai_memory:
                print(f"AI avoids snake at {new_position}!")
            else:
                new_position = self.snakes[new_position]
                if player_type == "ai":
                    self.ai_memory[new_position] = self.ai_memory.get(new_position, 0) + 1  # AI learns danger zones

        if new_position in self.ladders:
            new_position = self.ladders[new_position]

        if new_position in self.power_ups:
            self.activate_power_up(new_position, player_type)

        return new_position

    def ai_strategy(self, dice_roll):
        """AI adapts by avoiding frequently landed snake positions."""
        predicted_position = self.ai_position + dice_roll
        if predicted_position in self.snakes and self.ai_memory.get(predicted_position, 0) > 1:
            dice_roll = random.choice([1, 2, 3]) if random.random() < 0.7 else dice_roll
        return dice_roll

    def activate_power_up(self, position, player_type):
        """Handles activation of power-ups like teleportation, extra roll, and snake immunity."""
        power = self.power_ups[position]
        if power == "teleport":
            teleport_target = random.randint(position + 5, min(self.size, position + 20))
            print(f"{player_type.title()} teleported to {teleport_target}!")
            if player_type == "player":
                self.player_position = teleport_target
            else:
                self.ai_position = teleport_target
        elif power == "extra_roll":
            print(f"{player_type.title()} gets an extra roll!")
            if player_type == "player":
                self.player_position = self.move(self.player_position, "player")
            else:
                self.ai_position = self.move(self.ai_position, "ai")
        elif power == "snake_immunity":
            print(f"{player_type.title()} gained snake immunity!")
            if player_type == "ai":
                self.ai_memory["snake_immunity"] = True

    def play_game(self):
        """Runs the game loop with improved turn control and AI learning."""
        print(f"🎲 Welcome to Snakes and Ladders! Difficulty: {self.difficulty}")
        print(f"🐍 Snakes: {self.snakes}")
        print(f"🪜 Ladders: {self.ladders}")

        while True:
            print(f"\nPlayer at {self.player_position}, AI at {self.ai_position}")

            if self.turn == "player":
                input("Press Enter to roll...")
                self.player_position = self.move(self.player_position, "player")
                if self.player_position >= self.size:
                    print("\n🏆 Player wins the game!")
                    break
                self.turn = "ai"
            else:
                print("AI rolling...")
                self.ai_position = self.move(self.ai_position, "ai")
                if self.ai_position >= self.size:
                    print("\n🏆 AI wins the game!")
                    break
                self.turn = "player"
class RockPaperScissors:
    """
    Advanced Rock, Paper, Scissors game featuring an AI that learns player tendencies
    and occasionally bluffs with unexpected moves.
    """

    def __init__(self):
        """Initializes game settings, tracking systems, and AI behaviors."""
        self.choices = ["rock", "paper", "scissors"]
        self.score = {"player": 0, "computer": 0}
        self.history = []
        self.player_choice_count = {"rock": 0, "paper": 0, "scissors": 0}
        self.win_streak = 0
        self.main_menu()

    def get_computer_choice(self):
        """
        AI opponent predicts the player's most frequent move and counterpicks it,
        but sometimes **bluffs** to keep the player guessing.

        Returns:
            str: The AI's chosen move.
        """
        if random.random() < 0.25:  # 25% chance AI will bluff (play randomly)
            return random.choice(self.choices)
        
        if len(self.history) < 5:  # Early rounds are random
            return random.choice(self.choices)

        most_common_choice = max(self.player_choice_count, key=self.player_choice_count.get)
        counter_moves = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        return counter_moves[most_common_choice]  # AI counterpicks the player's habit

    def determine_winner(self, player, computer):
        """
        Determines the winner and applies the streak bonus.

        Args:
            player (str): Player's move ('rock', 'paper', or 'scissors').
            computer (str): Computer's move.

        Returns:
            str: Outcome message indicating win, loss, or tie.
        """
        self.player_choice_count[player] += 1  # Track player choice frequency

        if player == computer:
            self.win_streak = 0  # Streak resets on a tie
            return "It's a tie!"
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            self.win_streak += 1
            streak_bonus = min(self.win_streak, 5)  # Bonus caps at 5
            self.score["player"] += 1 + streak_bonus  # Apply streak bonus
            return f"You win! (Streak Bonus: +{streak_bonus})"
        else:
            self.win_streak = 0  # Streak resets on loss
            self.score["computer"] += 1
            return "Computer wins!"

    def play_round(self):
        """Handles a round against the AI opponent."""
        player_choice = input("\nChoose rock, paper, or scissors: ").lower()
        if player_choice not in self.choices:
            print("Invalid choice! Try again.")
            return
        
        computer_choice = self.get_computer_choice()
        print(f"Computer chose: {computer_choice}")

        result = self.determine_winner(player_choice, computer_choice)
        print(result)
        self.history.append((player_choice, computer_choice, result))

    def main_menu(self):
        """Displays the game menu with options."""
        while True:
            print("\n🎮 Rock, Paper, Scissors - Main Menu")
            print("1. Play Classic Mode (vs AI)")
            print("2. View Player Stats")
            print("3. Exit")

            choice = input("Select an option: ")
            if choice == "1":
                self.play_round()
            elif choice == "2":
                print(f"\n🔍 Player Stats: {self.player_choice_count}")
            elif choice == "3":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice! Try again.")
class Casino:
    def __init__(self, balance=100):
        self.balance = balance
        print(f"🎰 Welcome to the Casino! You start with ${self.balance}")
        self.play()

    def place_bet(self):
        while True:
            try:
                bet = int(input("Enter your bet amount: $"))
                if bet <= 0:
                    print("Bet must be greater than zero.")
                elif bet > self.balance:
                    print(f"Not enough funds! You have ${self.balance}.")
                else:
                    return bet
            except ValueError:
                print("Invalid amount, please enter a number.")

    def blackjack(self):
        print("\n♠️ Playing Blackjack!")
        bet = self.place_bet()
        
        # Simulating card drawing
        player_card = random.randint(15, 21)
        dealer_card = random.randint(15, 21)
        print(f"You draw {player_card}, Dealer draws {dealer_card}")
        
        if player_card > dealer_card:
            print("🎉 You win!")
            self.balance += bet
        elif player_card < dealer_card:
            print("💀 You lost!")
            self.balance -= bet
        else:
            print("😬 It's a tie!")

    def dice_roll(self):
        print("\n🎲 Rolling the Dice!")
        bet = self.place_bet()
        
        player_roll = random.randint(1, 6)
        casino_roll = random.randint(1, 6)
        print(f"You rolled {player_roll}, Casino rolled {casino_roll}")
        
        if player_roll > casino_roll:
            print("🎉 You win!")
            self.balance += bet
        else:
            print("💀 You lost!")
            self.balance -= bet

    def slot_machine(self):
        print("\n🎰 Spinning the Slot Machine!")
        bet = self.place_bet()
        
        slots = ["🍒", "🍋", "🔔", "⭐", "💎", "7️⃣"]
        result = [random.choice(slots) for _ in range(3)]
        print("🎲", result[0], result[1], result[2])
        
        if result[0] == result[1] == result[2]:
            print("🎉 Jackpot! 3 matching symbols!")
            self.balance += bet * 5
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            print("⭐ Small Win! 2 matching symbols!")
            self.balance += bet * 2
        else:
            print("💀 You lost!")
            self.balance -= bet

    def play(self):
        while self.balance > 0:
            print(f"\n💰 Your balance: ${self.balance}")
            choice = input("Choose a game (blackjack/dice/slots) or type 'exit': ").lower()
            if choice == "blackjack":
                self.blackjack()
            elif choice == "dice":
                self.dice_roll()
            elif choice == "slots":
                self.slot_machine()
            elif choice == "exit":
                print(f"🏆 You leave the casino with ${self.balance}. Goodbye!")
                break
            else:
                print("Invalid choice!")
class HandCricket:
    score = int
    def __init__(self):
        self.score = 0
        self.gameLoop()
    def gameLoop(self):
        print("Welcome to hand cricket.")
        print("Enter your choice:"
              "bat or bowl?")
        toss = input("You:").lower()
        if toss == "bat":
            print("You chose to bat!")
            while True:
                hand = int(input("Your hand:"))
                if hand>6 or hand<1:
                    print("Invalid hand.")
                    return
                self.battingForPlayer(hand)

        elif toss == "bowl":
            print("You chose to bowl!")
            while True:
                hand = int(input("Your hand:"))
                if hand>6 or hand<1:
                    print("Invalid hand.")
                    return
                self.bowlingForPlayer(hand)
        else:
            print("Invalid choice made.")

    def battingForPlayer(self,hand:int):
        computer = random.randint(1,6)
        print(f"Computer chose: {computer}")
        if computer == hand:
            print("Player lost!")
            print(f"Score: {self.score}")
            exit(0)
        else:
            self.score = self.score + hand
            print(f"Score: {self.score}")

    def bowlingForPlayer(self,ball):
        computer = random.randint(1,6)
        print(f"Computer chose: {computer}")
        if computer == ball:
            print("Player won!")
            print(f"Score: {self.score}")
            exit(0)
        else:
            self.score = self.score + computer
            print(f"Score: {self.score}")
class TicTacToe():
    """
    A simple command-line Tic Tac Toe game where a human plays against the computer.
    The board is a 3x3 grid. The player uses 'X' and the computer uses 'O'.
    """

    def __init__(self):
        """
        Initializes the game board and visited matrix.
        Starts the game loop.
        """
        self.board: list[list[str]] = [
            ["`","`","`"],
            ["`","`","`"],
            ["`","`","`"],
        ]
        self.visited: list[list[bool]] = [
            [False,False,False],
            [False,False,False],
            [False,False,False],
        ]
        print("\t\t\t\t-----Welcome to TICTACTOE!-----")
        self.gameLoop()

    def gameLoop(self):
        """
        Main game loop for alternating turns between the player and the computer.
        Handles user input, computer moves, win/draw checking, and board printing.
        """
        count = 0  # Counts the total number of moves
        while True:
            print("Enter the row no.")
            userRow = int(input("You: "))
            print("Enter the column no.")
            userCol = int(input("You: "))
            # Check if input is within valid range (1-3)
            if(0<userRow and userRow<4 and 0<userCol and userCol<4):
                if(self.updateBoard(userRow-1,userCol-1,"X")):
                    count+=1
                else:
                    print("Visited. Enter the coordinates again!")
                    continue
            else:
                return  # Exit if invalid input

            if(self.checkWinForPlayer()==True):
                print("Player won!")
                self.printBoard()
                return

            # Computer's turn
            computerMove = False
            while not computerMove:
                compRow = random.randint(0, 2)
                compCol = random.randint(0, 2)
                if(self.checkVisited(compRow,compCol)):
                    continue
                else:
                    self.updateBoard(compRow,compCol,"O")
                    count+=1
                    computerMove = True

            if(self.checkWinForComputer()):
                print("Computer won!")
                self.printBoard()
                return

            # Check for draw (all cells filled)
            if(count==8 and (not self.checkWinForComputer() or not self.checkWinForPlayer())):
                print("Its a draw!!")
                self.printBoard()
                return

            self.printBoard()

    def checkVisited(self, row: int, col: int) -> bool:
        """
        Checks if the cell at (row, col) has already been visited.
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
        Returns:
            bool: True if visited, False otherwise
        """
        return self.visited[row][col]
    
    def checkWinForPlayer(self) -> bool:
        """
        Checks if the player ('X') has won the game.
        Returns:
            bool: True if player wins, False otherwise
        """
        for i in range(0,3):
            # Check rows and columns for win
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == "X":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == "X":
                return True
        # Check diagonals for win
        if(self.board[0][0]==self.board[2][2] == self.board[1][1] == "X"):
            return True
        if(self.board[0][2] == self.board[1][1] == self.board[2][0] == "X"):
            return True
        return False

    def checkWinForComputer(self) -> bool:
        """
        Checks if the computer ('O') has won the game.
        Returns:
            bool: True if computer wins, False otherwise
        """
        for i in range(0,3):
            # Check rows and columns for win
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == "O":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == "O":
                return True
        # Check diagonals for win
        if(self.board[0][0]==self.board[2][2] == self.board[1][1] == "O"):
            print("D1")
            return True
        if(self.board[0][2] == self.board[1][1] == self.board[2][0] == "O"):
            print("D2")
            return True
        return False

    def updateBoard(self, row: int, col:int, prompt: str) -> bool:
        """
        Updates the board at (row, col) with the given prompt ('X' or 'O') if not already visited.
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            prompt (str): 'X' for player, 'O' for computer
        Returns:
            bool: True if update is successful, False if cell already visited
        """
        if(not self.checkVisited(row,col)):
            self.board[row][col] = prompt
            self.visited[row][col] = True
            return True
        return False

    def printBoard(self):
        """
        Prints the current state of the board to the console.
        """
        for row in self.board:
            print(*row)
def main():
    """
    Main menu for selecting which game to play.
    Uses match-case (Python 3.10+) for game selection.
    """
    print("\nWelcome to the Game Suite!")
    print("Select a game to play:")

    while True:
        print("1. Tic Tac Toe")
        print("2. Snakes and Ladders")
        print("3. Rock Paper Scissors")
        print("4. Casino")
        print("5. Hand Cricket")
        print("0. Exit")
        try:
            choice = int(input("Enter your choice (0-5): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                TicTacToe()
            case 2:
                SnakesLadders().play_game()
            case 3:
                RockPaperScissors()
            case 4:
                Casino()
            case 5:
                HandCricket()
            case 0:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()