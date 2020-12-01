import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class AnimalShogiNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(AnimalShogiNNet, self).__init__()
        
        self.board_layers = nn.Sequential(
            nn.Conv2d(1, args.num_channels, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
            nn.Conv2d(args.num_channels, args.num_channels, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
        )
        
        self.moti_layers = nn.Sequential(
            nn.Conv2d(1, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
            nn.ConvTranspose2d(512, 512, kernel_size = 2),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
        )
        
        self.layers2 = nn.Sequential(
            nn.Conv2d(args.num_channels*2, args.num_channels, 3, stride=1, padding=1),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
            nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1),
            nn.BatchNorm2d(args.num_channels),
            nn.ReLU(),
        )
        
        self.layers3 = nn.Sequential(
            nn.Linear(args.num_channels*2, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(),
        )

        self.fc0 = nn.Linear(512, self.action_size)

        self.fc1 = nn.Linear(512, 1)

    def forward(self, boards, motis):
        #                                                      boards: batch_size x 3 x 4
        #                                                       motis: batch_size x 2 x 3
        
        boards = boards.view(-1, 1, 3, 4)                            # batch_size x 1 x 3 x 4
        motis = motis.view(-1, 1, 2, 3)                                 # batch_size x 1 x 6
        
        boards = self.board_layers(boards)                           # batch_size x num_channels x 3 x 4
        motis = self.moti_layers(motis)                              # batch_size x num_channels x 3 x 4
        
        s = torch.cat((boards, motis), dim=1)                        # batch_size x (num_channels x 2) x 3 x 4
        s = self.layers2(s).view(-1, self.args.num_channels*2)       # batch_size x (num_channels x 2) x 12
        s = self.layers3(s)                                          # batch_size x 512

        pi = self.fc0(s)                                             # batch_size x action_size
        v = self.fc1(s)                                              # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
