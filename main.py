import logging

import coloredlogs

from Coach import Coach
from animalshogi.AnimalShogiGame import AnimalShogiGame as Game
from animalshogi.pytorch.NNet import NNetWrapper as nn
from utils import *

from animalshogi.AnimalShogiPlayers import RandomPlayer, HumanAnimalShogiPlayer, GreedyAnimalShogiPlayer
from Arena import Arena
from MCTS import MCTS
import numpy as np

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 10,
    'numEps': 10,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './ashogickpt/',
    'load_model': False,
    'load_folder_file': ('./ashogickpt/','best1.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
    'cuda': True,

})


def main():
    """
    nnet = nn(Game())
    nnet.load_checkpoint(folder='ashogickpt', filename='best.pth.tar')
    nmcts = MCTS(Game(), nnet, args)
    arena = Arena(HumanAnimalShogiPlayer(Game()).play, lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), Game(), Game().display)
    rwins, nwins, draws = arena.playGames(50)
    print('%d : %d (%d Draws)' % (nwins, rwins, draws))
    """

    log.info('Loading %s...', Game.__name__)
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file)
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
