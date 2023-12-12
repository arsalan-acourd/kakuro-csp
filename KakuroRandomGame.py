import random
import sys


class KakuroRandomGame(object):

    def __init__(self):
        self.played_so_far = []
        self.data_filled = []
        self.data_fills = []
        self.data_totals = []
        self.data_table = [['x'] * 9 for _ in range(9)]
        puzzlebank = []
        try:
            file = open("/Users/arsalan/PycharmProjects/pythonProject2/savedpuzzles.txt", "r")
        except IOError:
            print("Could not acquire read access to file: savedpuzzles.txt")
            sys.exit()
        with file:
            for line in file:
                if line.rstrip("\r\n").isdigit():
                    puzzlebank = puzzlebank + [int(line)]
            file.close()
        puzzlebank = [
            ele for ele in puzzlebank if ele not in self.played_so_far]
        numpuzzles = len(puzzlebank)
        if len(puzzlebank) == 0:
            print("Uh-Oh! You have exhausted the puzzle bank! Gather more puzzles!")
            sys.exit()
        print("There seem to be " + str(numpuzzles) +
              " unique untried puzzles this session!")
        print("Randomly picking one...")
        ctr = 0
        currprob = 1.0 / (numpuzzles - ctr)
        currguess = random.random()
        while currguess > currprob and ctr < numpuzzles - 1:
            ctr = ctr + 1
            currprob = 1.0 / (numpuzzles - ctr)
            currguess = random.random()
        self.gameId = puzzlebank[ctr]
        print("Selected puzzle: Number " +
              str(puzzlebank[ctr]) + ". Click anywhere on the grid to begin...")
        self.played_so_far = self.played_so_far + [self.gameId]
        file = open("/Users/arsalan/PycharmProjects/pythonProject2/savedpuzzles.txt", "r")
        readstatus = 0
        for line in file:
            if readstatus == 0 and line.rstrip("\r\n").isdigit():
                if int(line) == puzzlebank[ctr]:
                    readstatus = 1
                    continue
            if readstatus == 1 and line.rstrip("\r\n").isdigit():
                break
            elif readstatus == 1:
                line = line.rstrip("\r\n")
                if line[0] == 'e':
                    self.data_fills = self.data_fills + \
                                      [[int(line[1]), int(line[2])]]
                else:
                    self.data_totals = self.data_totals + \
                                       [[int(line[:-3]), line[-3], int(line[-2]), int(line[-1])]]
        file.close()
        for [i, j] in self.data_fills:
            self.data_table[i][j] = 0

        # print("self.data_fills :", self.data_fills,
        #       '\n-------------------------------------\n', "self.data_totals :", self.data_totals)
        self.game_over = False

    def check_win(self):
        if len(self.data_filled) == len(self.data_fills):
            for item in self.data_filled:
                if [item[0], item[1] - 1] not in self.data_fills:
                    sumexp = -1
                    for elem in self.data_totals:
                        if elem[2] == item[0] and elem[3] == item[1] - 1 and elem[1] == 'h':
                            sumexp = elem[0]
                    offset = 0
                    sumact = []
                    while [item[0], item[1] + offset] in self.data_fills:
                        sumact = sumact + \
                                 [e[2] for e in self.data_filled if e[0]
                                  == item[0] and e[1] == item[1] + offset]
                        offset = offset + 1
                    if len(sumact) != len(set(sumact)):
                        return False
                    if sumexp != -1 and sumexp != sum(sumact):
                        return False
            for item in self.data_filled:
                if [item[0] - 1, item[1]] not in self.data_fills:
                    sumexp = -1
                    for elem in self.data_totals:
                        if elem[2] == item[0] - 1 and elem[3] == item[1] and elem[1] == 'v':
                            sumexp = elem[0]
                    offset = 0
                    sumact = []
                    while [item[0] + offset, item[1]] in self.data_fills:
                        sumact = sumact + \
                                 [e[2] for e in self.data_filled if e[0]
                                  == item[0] + offset and e[1] == item[1]]
                        offset = offset + 1
                    if len(sumact) != len(set(sumact)):
                        return False
                    if sumexp != -1 and sumexp != sum(sumact):
                        return False
            return True
        else:
            return False