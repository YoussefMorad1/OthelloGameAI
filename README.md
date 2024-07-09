# AI Othello Game

This project is an interactive Othello game developed in Python, featuring both graphical and console-based user interfaces. It supports gameplay modes for human vs. human, human vs. AI, and AI vs. AI, showcasing a blend of GUI design, game logic, and AI implementation.

## Features

- **Dual Interface Options**: Play the game using either a graphical interface with Tkinter or a console-based interface.
- **AI Opponents**: Challenge AI players with varying difficulty levels (Easy, Medium, Hard, Very Hard) implemented using the Minimax algorithm with Alpha-Beta pruning.
- **Interactive Gameplay**: GUI highlights valid moves, provides real-time score updates, and announces the winner at the end of the game.
- **Error Handling**: Ensures smooth gameplay by handling invalid moves and situations with no valid moves gracefully.

## Gameplay Instructions

### GUI Mode

- Start the game by running the script.
- The GUI window will display the game board.
- Players take turns to click on valid board positions to place their pieces.
- The game will highlight valid moves and update the board accordingly.
- The scores and the current player's turn are displayed in the window title.

### Console Mode

- If playing in console mode, follow the on-screen prompts to enter moves.
- Players take turns to input their move coordinates in the format `X Y`.
- The console will display the current board state, valid moves, and scores.

## Code Overview

### Enums

- `Colors`: Enum for representing the state of each board cell (White, Black, Empty).
- `AIDifficulty`: Enum for representing AI difficulty levels.

### Classes

- `Board`: Handles the game board, move validation, and game logic.
- `BoardView`: Abstract base class for different board views (GUI, Console).
- `BoardViewConsole`: Implementation of the console-based interface.
- `BoardViewGUI`: Implementation of the graphical interface using Tkinter.
- `Game`: Manages the overall game flow, switching turns between players and checking for game end conditions.
- `Player`: Abstract base class for different player types (Human, AI).
- `HumanPlayer`: Handles input for human players.
- `AIPlayer`: Implements AI decision-making using the Minimax algorithm.
- `MiniMaxUtility`: Utility class for the Minimax algorithm with Alpha-Beta pruning.

### Preview

https://github.com/YoussefMorad1/OthelloGameAI/assets/102534922/d27d47d8-f92b-4fb9-b480-992986ad1357


