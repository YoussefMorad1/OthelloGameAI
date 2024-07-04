from Game import Game
from Players import HumanPlayer
from Views import BoardViewGUI
from enums import Colors

game = Game(BoardViewGUI(), HumanPlayer("Youssef", Colors.BLACK),
            HumanPlayer("Karim", Colors.WHITE))
game.play()
