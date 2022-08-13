import pygame as pg

class Move:
    def __init__(self, square1, square2, board):
        self.start_row = square1[0]
        self.start_col = square1[1]
        self.end_row = square2[0]
        self.end_col = square2[1]
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.end_row][self.end_col]

    def __eq__(self, other):
        if self.start_row == other.start_row and self.start_col == other.start_col and self.end_row == other.end_row and self.end_col == other.end_col and self.moved_piece == other.moved_piece and self.captured_piece == other.captured_piece:
            return True
        return False


class GameState:
    def __init__(self):
        self.white_turn = True
        self.move_log = []
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.move_made = False
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.moved_piece
        self.move_log.append(move)
        self.white_turn = not self.white_turn
        if move.moved_piece == "wk":
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.moved_piece == "bk":
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.moved_piece
            self.board[move.end_row][move.end_col] = move.captured_piece
            self.white_turn = not self.white_turn
            if move.moved_piece == "wk":
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.moved_piece == "bk":
                self.black_king_loc = (move.start_row, move.start_col)

    def undo_move_twice(self):
        if len(self.move_log) > 1:
            move1 = self.move_log.pop()
            move2 = self.move_log.pop()
            self.board[move1.start_row][move1.start_col] = move1.moved_piece
            self.board[move1.end_row][move1.end_col] = move1.captured_piece
            self.board[move2.start_row][move2.start_col] = move2.moved_piece
            self.board[move2.end_row][move2.end_col] = move2.captured_piece
            if move1.moved_piece == "wk":
                self.white_king_loc = (move1.start_row, move1.start_col)
            elif move1.moved_piece == "bk":
                self.black_king_loc = (move1.start_row, move1.start_col)
            if move2.moved_piece == "wk":
                self.white_king_loc = (move2.start_row, move2.start_col)
            elif move2.moved_piece == "bk":
                self.black_king_loc = (move2.start_row, move2.start_col)


    def all_possible_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                color = self.board[row][col][0]
                if color == "w":
                    enemy = "b"
                else:
                    enemy = "w"
                if (color == "w" and self.white_turn) or (color == "b" and (not self.white_turn)):
                    piece = self.board[row][col][1]
                    if piece == "p":
                        self.all_possible_pawn_moves(row, col, moves)
                    elif piece == "r":
                        self.all_possible_rook_moves(row, col, enemy, moves)
                    elif piece == "n":
                        self.all_possible_knight_moves(row, col, enemy, moves)
                    elif piece == "b":
                        self.all_possible_bishop_moves(row, col, enemy, moves)
                    elif piece == "q":
                        self.all_possible_queen_moves(row, col, enemy, moves)
                    elif piece == "k":
                        self.all_possible_king_moves(row, col, enemy, moves)
        return moves

    def all_possible_pawn_moves(self, row, col, moves):
        if self.white_turn:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col != 0:
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col != 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col != 0:
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col != 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def all_possible_rook_moves(self, row, col, enemy, moves):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in directions:
            for i in range(1, 8):
                row2 = row + i * direction[0]
                col2 = col + i * direction[1]
                if 0 <= row2 <= 7 and 0 <= col2 <= 7:
                    piece = self.board[row2][col2]
                    if piece == "--":
                        moves.append(Move((row, col), (row2, col2), self.board))
                    elif piece[0] == enemy:
                        moves.append(Move((row, col), (row2, col2), self.board))
                        break
                    else:
                        break
                else:
                    break

    def all_possible_knight_moves(self, row, col, enemy, moves):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for direction in directions:
            row2 = row + direction[0]
            col2 = col + direction[1]
            if 0 <= row2 <= 7 and 0 <= col2 <= 7:
                piece = self.board[row2][col2]
                if piece == "--" or piece[0] == enemy:
                    moves.append(Move((row, col), (row2, col2), self.board))

    def all_possible_bishop_moves(self, row, col, enemy, moves):
        directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        for direction in directions:
            for i in range(1, 8):
                row2 = row + i * direction[0]
                col2 = col + i * direction[1]
                if 0 <= row2 <= 7 and 0 <= col2 <= 7:
                    piece = self.board[row2][col2]
                    if piece == "--":
                        moves.append(Move((row, col), (row2, col2), self.board))
                    elif piece[0] == enemy:
                        moves.append(Move((row, col), (row2, col2), self.board))
                        break
                    else:
                        break
                else:
                    break

    def all_possible_queen_moves(self, row, col, enemy, moves):
        self.all_possible_rook_moves(row, col, enemy, moves)
        self.all_possible_bishop_moves(row, col, enemy, moves)

    def all_possible_king_moves(self, row, col, enemy, moves):
        directions = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
        for direction in directions:
            row2 = row + direction[0]
            col2 = col + direction[1]
            if 0 <= row2 <= 7 and 0 <= col2 <= 7:
                piece = self.board[row2][col2]
                if piece == "--" or piece[0] == enemy:
                    moves.append(Move((row, col), (row2, col2), self.board))

    def all_legal_moves(self):
        legal_moves = self.all_possible_moves()
        for i in range(len(legal_moves) - 1, -1, -1):
            self.make_move(legal_moves[i])
            self.white_turn = not self.white_turn
            if self.in_check():
                legal_moves.remove(legal_moves[i])
            self.white_turn = not self.white_turn
            self.undo_move()
        if len(legal_moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return legal_moves

    def in_check(self):
        if self.white_turn:
            return self.square_attacked(self.white_king_loc[0], self.white_king_loc[1])
        else:
            return self.square_attacked(self.black_king_loc[0], self.black_king_loc[1])


    def square_attacked(self, row, col):
        self.white_turn = not self.white_turn
        moves = self.all_possible_moves()
        self.white_turn = not self.white_turn
        for move in moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def evaluation(self):
        sum = 0
        pieces_dic = {"p":100, "n":320, "b":330, "r":500, "q":900, "k":20000}
        if self.check_mate:
            if self.white_turn:
                return -20000
            else:
                return 20000
        if self.stale_mate:
            return 0

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col][1]
                color = self.board[row][col][0]
                if piece != "-":
                    if color == "w":
                        sum = sum + pieces_dic[piece]
                    else:
                        sum = sum - pieces_dic[piece]
        return sum

def load_images():
    pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
    for piece in pieces:
        Images_Dic[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (Square_Size, Square_Size))


def draw_game_state(screen, game_state, valid, selected_square):
    draw_board(screen)
    draw_highlight(screen, game_state, valid, selected_square)
    draw_pieces(screen, game_state.board)


def draw_board(screen):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = pg.Color("white")
            else:
                color = pg.Color("brown")
            pg.draw.rect(screen, color, pg.Rect(col*Square_Size, row*Square_Size, Square_Size, Square_Size))


def draw_highlight(screen, game_state, valid, selected_square):
    if selected_square != ():
        row, col = selected_square
        if game_state.board[row][col][0] == "w":
            s = pg.Surface((Square_Size, Square_Size))
            s.set_alpha(100)
            s.fill(pg.Color("green"))
            screen.blit(s, (col*Square_Size, row*Square_Size))
            s.fill(pg.Color("yellow"))
            for move in valid:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col*Square_Size, move.end_row*Square_Size))


def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                screen.blit(Images_Dic[piece], pg.Rect(col*Square_Size, row*Square_Size, Square_Size, Square_Size))

def optimal_move(game_state):
    depth = 3
    if game_state.white_turn:
        best = minimax(game_state, depth, float("-inf"), float("inf"), True)
    else:
        best = minimax(game_state, depth, float("-inf"), float("inf"), False)
    return best[1]

def minimax(game_state, depth, alpha, beta, is_maximizing):
    valid = game_state.all_legal_moves()
    if depth == 0 or game_state.check_mate or game_state.stale_mate:
        return game_state.evaluation(), None
    if is_maximizing:
        best_move = None
        for move in valid:
            game_state.make_move(move)
            (temp_score, temp_move) = minimax(game_state, depth - 1, alpha, beta, False)
            game_state.undo_move()
            if temp_score > alpha:
                alpha = temp_score
                best_move = move
                if alpha >= beta:
                    break
        return alpha, best_move
    else:
        best_move = None
        for move in valid:
            game_state.make_move(move)
            (temp_score, temp_move) = minimax(game_state, depth - 1, alpha, beta, True)
            game_state.undo_move()
            if temp_score < beta:
                beta = temp_score
                best_move = move
                if alpha >= beta:
                    break
        return beta, best_move

def main():
    pg.init()
    screen = pg.display.set_mode((Screen_Size, Screen_Size))
    screen.fill(pg.Color("white"))
    game_state = GameState()
    load_images()
    selected_square = ()
    selections = []
    valid = game_state.all_legal_moves()
    run = True
    while run:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_u:
                    game_state.undo_move_twice()
                    game_state.move_made = True
                    selected_square = ()
                    selections = []
                    break
            if game_state.white_turn:
                if e.type == pg.MOUSEBUTTONDOWN:
                    loc = pg.mouse.get_pos()
                    col = loc[0] // Square_Size
                    row = loc[1] // Square_Size
                    if len(selections) == 0:
                        if game_state.board[row][col][0] == "w":
                            selected_square = (row, col)
                            selections.append(selected_square)
                    else:
                        selected_square = (row, col)
                        move1 = Move(selections[0], selected_square, game_state.board)
                        if move1 in valid:
                            game_state.make_move(move1)
                            game_state.move_made = True
                            selected_square = ()
                            selections = []
                        else:
                            if move1.captured_piece == "--" or move1.captured_piece[0] == "b" or (move1.start_row == move1.end_row and move1.start_col == move1.end_col):
                                selected_square = ()
                                selections = []
                            else:
                                selections[0] = selected_square
            else:
                best = optimal_move(game_state)
                game_state.make_move(best)
                game_state.move_made = True

        if game_state.move_made:
            valid = game_state.all_legal_moves()
            game_state.move_made = False
        draw_game_state(screen, game_state, valid, selected_square)
        pg.display.flip()


Screen_Size = 552
Square_Size = Screen_Size // 8
FPS = 15
Images_Dic = {}
main()
