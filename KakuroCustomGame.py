class KakuroError(Exception):
    pass

class KakuroCustomGame(object):
    """
    A Kakuro game. Stores gamestate and completes the puzzle as needs be
    """

    def __init__(self):
        self.played_so_far = []
        self.data_filled = []
        self.data_fills = []
        self.data_totals = []
        print('Enter 9 lines. Use format described in README.')
        try:
            for i in range(9):
                text = raw_input()
                proced = [ele.split('\\') for ele in text.split(',')]
                if len(proced) != 9:
                    raise KakuroError('Nine cells a line or else format not followed!\n')
                for j in range(9):
                    if len(proced[j]) == 1 and proced[j][0] == ' ':
                        self.data_fills = self.data_fills + [[i, j]]
                    elif len(proced[j]) == 2:
                        if proced[j][0] != ' ':
                            self.data_totals = self.data_totals + [[int(proced[j][0]), 'v', i, j]]
                        if proced[j][1] != ' ':
                            self.data_totals = self.data_totals + [[int(proced[j][1]), 'h', i, j]]
        except ValueError:
            raise KakuroError('Format not followed! Integers only otherwise something else')
        print('\nStarting custom game. Click anywhere on the grid to begin...')
        self.gameId = 0
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
                        sumact = sumact + [e[2] for e in self.data_filled if
                                           e[0] == item[0] and e[1] == item[1] + offset]
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
                        sumact = sumact + [e[2] for e in self.data_filled if
                                           e[0] == item[0] + offset and e[1] == item[1]]
                        offset = offset + 1
                    if len(sumact) != len(set(sumact)):
                        return False
                    if sumexp != -1 and sumexp != sum(sumact):
                        return False
            return True
        else:
            return False