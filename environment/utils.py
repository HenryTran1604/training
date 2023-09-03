FPS = 60
FIELD_COLOR = ( 48, 39, 32) # Màu nền 
BG_COLOR = (24, 89, 117)

FONT_PATH = 'assets/font/FREAKSOFNATUREMASSIVE.ttf'

TILE_SIZE = 30 # kích thước 1 khối
FIELD_SIZE = FIELD_W, FIELD_H = 10, 22 # số khối ngang dọc
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE # kích thước vùng chơi

FIELD_SCALE_W, FIELD_SCALE_H = 1.8, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H



COLORS = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
TETROMINOES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]
def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False
def remove_row(board, row):
    del board[row]
    return [[0 for i in range(FIELD_W)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1    ][cx+off_x] += val
    return mat1

def new_board():
    board = [[0 for x in range(FIELD_W) ]
            for y in range(FIELD_H) ]
    #board += [[ 1 for x in range(FIELD_W)]]
    return board