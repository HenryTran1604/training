import random
import numpy as np
from environment.ai import Ai
import pygame, sys
from environment.utils import *

import pygame.freetype as ft

class Frame(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.default_font = ft.Font(FONT_PATH)

        self.screen = pygame.display.set_mode(WIN_RES)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.time.set_timer(pygame.USEREVENT+1, 200)

    def draw_background(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def disp_msg(self, msg, fcolor, topleft, size):
        x,y = topleft
        for line in msg.splitlines():
            self.default_font.render_to(self.screen, (x, y),
                text=line, fgcolor=fcolor, size=size, bgcolor=None)
            y+=14

    def center_msg(self, msg):
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *WIN_RES))
        for i, line in enumerate(msg.splitlines()):
            text_surface, _ = self.default_font.render(line, (255, 0, 255), size=30)
            text_rect = text_surface.get_rect(center=(WIN_W // 2, WIN_H//3 + i * 45))
            self.screen.blit(text_surface, text_rect)

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,COLORS[val],
                        pygame.Rect((off_x+x) * TILE_SIZE, (off_y+y) * TILE_SIZE,
                            TILE_SIZE, TILE_SIZE),0)

    def update(self, tetris):
        self.screen.fill(color=BG_COLOR) # set màu nền
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        if tetris.gameover:# or self.nbPiece >= maxPiece:
            self.center_msg("""Game Over!\nYour score: %d\nCompleted lines: %d\nPress space to continue""" % (tetris.score, tetris.lines))
        else:
            if tetris.paused:
                self.center_msg("Paused")
            else:
                pygame.draw.line(self.screen, (255,255,255), (FIELD_RES[0]+1, 0), (FIELD_RES[0]+1, WIN_H-1))
                self.disp_msg("Next", 'white', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE), 30*1.1)
                self.disp_msg('Score', 'white', (FIELD_RES[0]+TILE_SIZE, TILE_SIZE*7), 30*1.1)
                self.disp_msg(str(tetris.score), 'orange', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 9), 30)
                self.disp_msg('Level', 'white', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 11), 30*1.1)
                self.disp_msg(str(tetris.level), 'orange',(FIELD_RES[0] + TILE_SIZE*2, TILE_SIZE * 13), 30*1.1)

                self.disp_msg('Lines', 'white',(FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 15), 30*1.1)
                self.disp_msg(str(tetris.lines), 'orange',(FIELD_RES[0] + TILE_SIZE*2, TILE_SIZE * 17), 30*1.1)

                self.disp_msg('Mode: User' if tetris.user else 'Mode: AI', 'white',(FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 19), 25)
                self.draw_background()
                self.draw_matrix(tetris.board, (0,0))
                self.draw_matrix(tetris.tetromino, (tetris.tetromino_x, tetris.tetromino_y))
                self.draw_matrix(tetris.next_tetromino, (FIELD_W+2,3))
        pygame.display.update()



class Tetris(object):
    
    def __init__(self, user, display, seed):
        self.user = user
        self.nbPiece = 0
        random.seed(seed)
        self.next_tetromino = TETROMINOES[random.randint(0, len(TETROMINOES)-1)]
        self.display = display
        self.fast_mode = not user
        if display:
            self.frame = Frame()
        self.gameover = False
        self.paused = False

        self.init_game()

    def new_tetromino(self):
        self.tetromino = self.next_tetromino[:]
        self.next_tetromino = TETROMINOES[random.randint(0, len(TETROMINOES)-1)]
        self.tetromino_x = int(FIELD_W / 2 - len(self.tetromino[0])/2)
        self.tetromino_y = 0
        self.nbPiece += 1
        self.computed = False

        if check_collision(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_tetromino()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.combo = -1
        self.sent = 0
        self.pre_back2back = 0
        self.now_back2back = 0
        self.tetris = 0

    def switch_mode(self):
        self.user = not self.user

    def sent_lines(self, cleared):
        if cleared == 0:
            scores = 0
        else:
            scores = cleared if cleared == 4 else cleared - 1

            # scores from combos
            if self.combo > 0:
                if self.combo <= 8:
                    combo_scores = int((self.combo + 1) / 2)
                else: combo_scores = 4
            else:
                combo_scores = 0

            scores += combo_scores

            if self.pre_back2back:
                if  tetris:
                    scores += 2
        return scores
    
    def add_cl_lines(self, cleared):
        if cleared >= 1: # for sending lines
            self.combo += 1
            if cleared == 4: # a tetris
                self.tetris = 1
            else:
                self.tetris = 0

            self.pre_back2back = self.now_back2back   
        else:
            self.combo = -1
            self.tetris = 0
        if cleared >= 1:
            if self.tetris:
                print("next backtoback")
                self.now_back2back = 1
            else:
                self.now_back2back = 0
        now_sent_lines = self.sent_lines(cleared)
        linescores = [0, 40, 100, 300, 1200]
        self.lines += cleared
        self.sent += now_sent_lines
        self.score += linescores[cleared] * self.level
        if self.lines >= self.level*6:
            self.level += 1

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.tetromino_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > FIELD_W - len(self.tetromino[0]):
                new_x = FIELD_W - len(self.tetromino[0])
            if not check_collision(self.board, self.tetromino, (new_x, self.tetromino_y)):
                self.tetromino_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.tetromino_y += 1
            if check_collision(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y)):
                self.board = join_matrixes(self.board, self.tetromino, (self.tetromino_x, self.tetromino_y))
                self.new_tetromino()
                cleared_rows = 0

                for i, row in enumerate(self.board):
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        cleared_rows += 1
                        # print('cleared rows: ', cleared_rows)
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def instance_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_tetromino(self):
        if not self.gameover and not self.paused:
            new_tetromino = rotate_clockwise(self.tetromino)
            if not check_collision(self.board, new_tetromino, (self.tetromino_x, self.tetromino_y)):
                self.tetromino = new_tetromino

    def pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def quit(self):
        if self.display:
            pygame.display.update()
        sys.exit()

    def speed_up(self):
        self.fast_mode = not self.fast_mode
        if self.fast_mode:
            pygame.time.set_timer(pygame.USEREVENT+1, 25)
        else:
            pygame.time.set_timer(pygame.USEREVENT+1, 100)


    def executes_moves(self, moves):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_tetromino,
            'p':        self.pause,
            'SPACE':    self.start_game,
            'RETURN':    self.instance_drop
        }
        for action in moves:
            key_actions[action]()

        if self.fast_mode:
            self.instance_drop()


    def run(self, weights, limitPiece):
        self.gameover = False
        self.paused = False
        while 1:
            #for training
            if self.nbPiece >= limitPiece and limitPiece > 0:
                self.gameover = True

            if self.display:
                self.frame.update(self)

            # for training
            if not self.user and limitPiece > 0 and self.gameover:
                print('\n----------------------------------')
                print('  sent           :', self.sent)
                print('  used block     :', self.nbPiece)
                print('  complete lines :', self.lines)
                print('----------------------------------')
                return self.sent * 5000 + self.lines*1000 + self.nbPiece
            if not self.user and not self.computed:
                # print(self.computed)
                self.computed = True
                Ai.choose(self.board, self.combo, self.pre_back2back, self.tetromino, self.next_tetromino, self.tetromino_x, weights, self)
            if self.display:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.USEREVENT+1:
                        self.drop(False)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move(-1)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1)
                        elif event.key == pygame.K_UP:
                            self.rotate_tetromino()
                        elif event.key == pygame.K_DOWN:
                            self.instance_drop()
                        elif event.key == pygame.K_p:
                            self.pause()
                        elif event.key == pygame.K_SPACE and self.gameover:
                            self.start_game()
                        elif event.key == pygame.K_u:
                            self.switch_mode()
                        elif event.key == pygame.K_s:
                            self.speed_up()
            
if __name__ == '__main__':
    # weights = [-7.729900101782016, 2.839002198171473, -8.114470728396613, -3.788259232308481]
    weights = np.loadtxt('weights/optimal.txt')
    tetris = Tetris(user=False, display=True, seed=4).run(weights, -1)
