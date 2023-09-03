from field import Field
import copy
from utils import *
class Ai:

    @staticmethod
    def best(field, workingPieces, workingPieceIndex, weights, level):
        bestRotation = None
        bestOffset = None
        bestScore = None
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]
        shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }
        flat_piece = [val for sublist in workingPiece for val in sublist]
        hashedPiece = sum(flat_piece)

        for rotation in range(0, shapes_rotation[hashedPiece]):
            for offset in range(0, FIELD_W):
                result = field.project_piece_down(workingPiece, offset, level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces)-1 :
                        heuristics = field.heuristics()
                        score = sum([a*b for a,b in zip(heuristics, weights)])
                    else:
                        _, _, score = Ai.best(field, workingPieces, workingPieceIndex + 1, weights, 2)

                    if bestScore is None or score > bestScore:
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                field.undo(level)
            workingPiece = rotate_clockwise(workingPiece)

        return bestOffset, bestRotation, bestScore

    @staticmethod
    def choose(initialField, combo, pre_back2back, piece, next_piece, offsetX, weights, parent):
        field = Field(combo, pre_back2back)
        field.update_field(copy.deepcopy(initialField))
        offset, rotation, _ = Ai.best(field, [piece, next_piece], 0, weights, 1)
        moves = []
        offset = offset - offsetX
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        parent.executes_moves(moves)
