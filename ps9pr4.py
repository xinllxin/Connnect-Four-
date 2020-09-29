#
# ps9pr4.py  (Problem Set 9, Problem 4)
#
# AI Player for use in Connect Four
#

import random
from ps9pr3 import *

class AIPlayer(Player):
    '''subclass of the Player class'''

    def __init__(self,checker,tiebreak,lookahead):
        ''' tiebreak that stores a string specifying the player’s
            tiebreaking strategy ('LEFT', 'RIGHT', or 'RANDOM')
            lookahead that stores an integer specifying how many
            moves the player looks ahead in order to evaluate possible moves.
        '''

        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead

    def __repr__(self):
        ''' This method will override/replace the __repr__ method that is
            inherited from Player. In addition to indicating which checker the
            AIPlayer object is using, the returned string should also indicate
            the player’s tiebreaking strategy and lookahead.
        '''
        s = super().__repr__()
        new_s = s + ' (' + self.tiebreak +', '+ str(self.lookahead) +')'
        return new_s



    def max_score_column(self, scores):
        ''' takes a list scores containing a score for each column of the board,
            and that returns the index of the column with the maximum score. If one
            or more columns are tied for the maximum score, the method should apply
            the called AIPlayer‘s tiebreaking strategy to break the tie. Make sure
            that you return the index of the appropriate column, and not the column’s
            score.
        '''
        max_scores_indices = []
        for i in range(len(scores)):
            if scores[i] == max(scores):
                max_scores_indices += [i]


        if self.tiebreak == 'LEFT':
            return max_scores_indices[0]
        elif self.tiebreak == 'RIGHT':
            return max_scores_indices[-1]
        else:
            import random
            return random.choice(max_scores_indices)

    def scores_for(self,b):
        ''' takes a Board object b and determines the called AIPlayer‘s scores
            for the columns in b. Each column should be assigned one of the four
            possible scores discussed in the Overview at the start of this problem,
            based on the called AIPlayer‘s lookahead value. The method should return
            a list containing one score for each column.
        '''
        scores = [ [s] for s in range(b.width)]

        for c in range(b.width):

            if not b.can_add_to(c):
                scores[c] = -1
            elif b.is_win_for(self.checker):
                scores[c] = 100
            elif b.is_win_for(super().opponent_checker()):
                scores[c] = 0
            elif self.lookahead == 0:
                scores[c] = 50
            else:
                b.add_checker(self.checker,c) #temporary checker
                opponent = AIPlayer(super().opponent_checker(),self.tiebreak,self.lookahead -1)
                opponent_scores = opponent.scores_for(b)
                if max(opponent_scores) == 100:
                    scores[c] = 0
                elif max(opponent_scores) == 0:
                    scores[c] = 100
                elif max(opponent_scores) == 50:
                    scores[c] = 50
                b.remove_checker(c) #remove temporary checker

        return scores


    def next_move(self, b):
        ''' overrides the next_move method inherited from Player. use scores_for
                and max_score_column methods to determine the column number that should be
                returned. increment the number of num_moves
        '''
            #coloum with max score

        column = self.max_score_column(self.scores_for(b))
        self.num_moves += 1
        return column
