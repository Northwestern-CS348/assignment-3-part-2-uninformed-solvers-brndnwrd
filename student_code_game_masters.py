from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        #disk_states: list of bindings of disks to pegs
        disk_states = self.kb.kb_ask(parse_input('fact: (on ?x ?y'))

        big_list = []

        for peg in range(1, 4):
            peg_list = []
            peg_name = 'peg' + str(peg)
            if self.kb.kb_ask(Fact(Statement(['empty', peg_name]))):
                big_list.append(tuple(peg_list))
                continue
            for disk in range(1, len(disk_states)+1):
                disk_name = 'disk' + str(disk)
                if self.kb.kb_ask(Fact(Statement(['on', disk_name, peg_name]))):
                    peg_list.append(disk)
            peg_list.sort()
            big_list.append(tuple(peg_list))

        return tuple(big_list)

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        disk = movable_statement.terms[0]
        start = movable_statement.terms[1]
        end = movable_statement.terms[2]

        self.kb.kb_retract(Fact(Statement(['on', disk, start])))
        self.kb.kb_retract(Fact(Statement(['top', start, disk])))

        unders = self.kb.kb_ask(Fact(Statement(['over', disk, '?z'])))
        if unders:
            under = unders[0].bindings_dict['?z']
            self.kb.kb_retract(Fact(Statement(['over', disk, under])))
            self.kb.kb_assert(Fact(Statement(['top', start, under])))
        else:
            self.kb.kb_assert(Fact(Statement(['empty', start])))

        if self.kb.kb_ask(Fact(Statement(['empty', end]))):
            self.kb.kb_retract(Fact(Statement(['empty', end])))
        else:
            new_under = self.kb.kb_ask(Fact(Statement(['top', end, '?w'])))[0].bindings_dict['?w']
            self.kb.kb_retract(Fact(Statement(['top', end, new_under])))
            self.kb.kb_assert(Fact(Statement(['over', disk, new_under])))

        self.kb.kb_assert(Fact(Statement(['on', disk, end])))
        self.kb.kb_assert(Fact(Statement(['top', end, disk])))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        big_list = [[0,0,0], [0,0,0], [0,0,0]]

        locs = self.kb.kb_ask(Fact(Statement(['location', '?t', '?x', '?y'])))
        for tile in locs:
            y = int(tile.bindings_dict['?y'][-1])-1
            x = int(tile.bindings_dict['?x'][-1])-1
            val = tile.bindings_dict['?t'][-1]
            if val == 'y':
                val = -1
            big_list[y][x] = int(val)
        return tuple(tuple(row) for row in big_list)

        ### Old getGameState
        # for y in range(1, 4):
        #     posy = "pos" + str(y)
        #     row = []
        #     for x in range(1, 4):
        #         posx = "pos" + str(x)
        #         tile = self.kb.kb_ask(parse_input('fact: (location ?t ' + posx + ' ' + posy + ')'))
        #         value = tile[0].bindings_dict['?t'][-1]
        #         if value == 'y':
        #             value = -1
        #         row.append(int(value))
        #     big_list.append(tuple(row))
        # return tuple(big_list)

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        t = movable_statement.terms

        self.kb.kb_retract(Fact(Statement(['location', t[0], t[1], t[2]])))
        self.kb.kb_retract(Fact(Statement(['location', 'empty', t[3], t[4]])))

        self.kb.kb_assert(Fact(Statement(['location', t[0], t[3], t[4]])))
        self.kb.kb_assert(Fact(Statement(['location', 'empty', t[1], t[2]])))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
