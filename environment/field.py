
from utils import *
import numpy as np
class Field:
    def __init__(self, combo, pre_back2back):
        self.field = [[0]*FIELD_W]*FIELD_H
        self.combo = combo
        self.pre_back2back = pre_back2back

    def size(self):
        return FIELD_W, FIELD_H

    def update_field(self, field):
        self.field = field

    

    def project_piece_down(self, piece, offsetX, workingPieceIndex):
        if offsetX+len(piece[0]) > FIELD_W or offsetX < 0:
            return None
        #result = copy.deepcopy(self)
        offsetY = FIELD_H
        for y in range(0, FIELD_H):
            if check_collision(self.field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(0, len(piece[0])):
            for y in range(0, len(piece)):
                value = piece[y][x]
                if value > 0:
                    self.field[offsetY-1+y][offsetX+x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.field = [[0 if el == -workingPieceIndex else el for el in row] for row in self.field]

    def heightForColumn(self, column):
        width, height = self.size()
        for i in range(0, height):
            if self.field[i][column] != 0:
                return height-i
        return 0

    def heights(self):
        result = []
        width, height = self.size()
        for i in range(0, width):
            result.append(self.heightForColumn(i))
        return result

    ################################################
    #                   HEURISTICS                 #
    ################################################

    def heuristics(self):
        heights = self.heights()
        return [
            self.complete_line(),
            self.send_lines(),
            self.aggregate_height(heights),
            self.number_of_holes(heights),
            self.bumpinesses(heights),
            self.max_height_columns(heights),
            self.min_height_columns(heights),
            self.max_pit_depth(heights)
        ] #         10   +        1 +                    +       10 +                        10                      +                    4 
    def aggregate_height(self, heights):
        result = sum(heights)
        return result

    def complete_line(self):
        result = 0
        width, height = self.size()
        for i in range (0, height) :
            if 0 not in self.field[i]:
                result+=1
        return result

    def send_lines(self):
        cleared = self.complete_line()
        if cleared == 0:
            scores = 0
        else:
            tetris, scores = (cleared, 1) if cleared == 4 else (cleared - 1, 0)
            # Nếu ăn 4 hàng thì score = 4 ngược lại bằng số hàng clear - 1

            # scores from combos
            if self.combo > 0:
                if self.combo <= 8:
                    # Số combo mà nhỏ hơn 8 thì điểm cộng bằng 1/2 combo
                    combo_scores = int((self.combo + 1) / 2)
                else: combo_scores = 4
            else:
                combo_scores = 0

            scores += combo_scores

            if self.pre_back2back:
                if tetris:
                    scores += 2
        return scores

    def bumpinesses(self, heights):
        result = 0
        for i in range(0, len(heights)-1):
            result += abs(heights[i]-heights[i+1])
        return result

    def number_of_holes(self, heights):
        result = 0
        width, height = self.size()
        for j in range(0, width) :
            result = 0
            for i in range (0, height) :
                if self.field[i][j] == 0 and height-i < heights[j]:
                    result+=1
        return result

    def max_height_columns(self, heights):
        return max(heights)

    def min_height_columns(self, heights):
        return min(heights)


    def max_pit_depth(self, heights):
        return max(heights)-min(heights)
