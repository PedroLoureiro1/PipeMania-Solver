# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 63:
# 107059 Pedro Loureiro
# 106930 André Bento

#import time
import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
current_piece = (0,0)
flag_reset = 0

flag_corners = 0  #simboliza se algum está correto

#Auxiliar lists to check if the pieces connect

list_lef= ['FC', 'FB', 'FE', 'BE', 'VE', 'VC','LV']  #belongs to the list
list_righ = ['FC', 'FB', 'FD', 'BD', 'VB', 'VD','LV']  #belongs to the list
list_u = ['FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH']  #belongs to the list
list_dow = ['FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH']  #belongs to the list

list_left = np.array(list_lef)
list_right = np.array(list_righ)
list_up = np.array(list_u)
list_down = np.array(list_dow)

def create_zero_initialized_board(rows, cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board  
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def get_board(self):
        """Getter method for the board attribute."""
        return self.board
    
    def __str__(self):
        """String representation of the PipeManiaState."""
        return str(self.board)
    
    def id(self):
        return PipeManiaState.state_id
    
    # TODO: outros metodos da classe


class Board: #printar o board sem flag ehehe
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        # Join each row with tab characters and concatenate them with newline characters
        return '\n'.join(['\t'.join([piece[:2] for piece in row]) for row in self.rows])
    
    def get_full_piece(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.rows[row][col]
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.rows[row][col][:2]
    
    def get_piece_type(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.rows[row][col][0]
    
    def get_piece_orien(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.rows[row][col][1]
    
    def get_flag(self, row: int, col: int) -> int:
        if col > len(self.rows) - 1 or col < 0:
            return '555'
        
        if row > len(self.rows) - 1 or row < 0:
            return '555'
        
        return self.rows[row][col][2]

    
    def set_flag(self, row: int, col: int, flag: int):
         # Get the current string at the specified position
        current_string = self.rows[row][col]

        # Modify the third character to be the flag
        new_string = current_string[:2] + str(flag)  # Combine the first two characters with the flag

        # Update the value in the rows list
        self.rows[row][col] = new_string
    
    
    def set_value(self, row: int, col: int, value):
        """Set the value of the cell at the specified row and column."""
        current_value = self.rows[row][col]
        new_value = value + current_value[2:]  # Extract first two characters from value and concatenate with unchanged number part
        self.rows[row][col] = new_value
    
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row > 0:
            above_value = self.rows[row - 1][col][:2]
        else:
            above_value = None

        if row < len(self.rows) - 1:
            below_value = self.rows[row + 1][col][:2]
        else:
            below_value = None

        #return f'({above_value}, {below_value})'
        return above_value, below_value

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col > 0:
            left_value = self.rows[row][col - 1][:2]
        else:
            left_value = None

        if col < len(self.rows) - 1:
            right_value = self.rows[row][col + 1][:2]
        else:
            right_value = None

        #return f'({left_value}, {right_value})'
        return left_value,right_value

    def adj_vert_full(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row > 0:
            above_value = self.rows[row - 1][col]
        else:
            above_value = '555'

        if row < len(self.rows) - 1:
            below_value = self.rows[row + 1][col]
        else:
            below_value = '555'

        #return f'({above_value}, {below_value})'
        return above_value, below_value

    def adj_hori_full(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col > 0:
            left_value = self.rows[row][col - 1]
        else:
            left_value = '555'

        if col < len(self.rows) - 1:
            right_value = self.rows[row][col + 1]
        else:
            right_value = '555'

        #return f'({left_value}, {right_value})'
        return left_value,right_value

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        rows = []
        for line in sys.stdin.readlines():
            line = line.strip()  # Remove leading/trailing whitespace and newline characters
            values = line.split('\t')  # Split values on the tab character
            rows.append([value + '0' for value in values])
        return Board(rows)
    
    def corners(self):
        """adjusts the values of the corners."""
        global flag_corners
        height = len(self.rows)
        width = len(self.rows[0]) if self.rows else 0

        top_left = self.rows[0][0][:2]
        top_right = self.rows[0][width - 1][:2]
        bottom_left = self.rows[height - 1][0][:2]
        bottom_right = self.rows[height - 1][width - 1][:2]
        
        if top_left[0] == 'F':
            _, right_adj = self.adjacent_horizontal_values(0,0)
            _, down_adj = self.adjacent_vertical_values(0,0)
            
            if right_adj[0] == 'F' or down_adj[0] in ['B', 'L']:
                self.set_value(0,0,'FB')
                self.set_flag(0,0,1)
                flag_corners = 1
            elif down_adj[0] == 'F' or right_adj[0] in ['B', 'L']:
                self.set_value(0,0, 'FD')
                self.set_flag(0,0,1)
                flag_corners = 1
            else:
                self.set_value(0,0,'FB')
        else:
            self.set_value(0,0,'VB')
            self.set_flag(0,0,1)
            flag_corners = 1
            
        if top_right[0] == 'F':
            left_adj, _ = self.adjacent_horizontal_values(0,width - 1)
            _, down_adj = self.adjacent_vertical_values(0,width - 1)
            
            if left_adj[0] == 'F' or down_adj[0] in ['B', 'L']:
                self.set_value(0, width - 1,'FB')
                self.set_flag(0,width - 1,1)
                flag_corners = 1
            elif down_adj[0] == 'F' or left_adj[0] in ['B', 'L']:
                self.set_value(0, width - 1, 'FE')
                self.set_flag(0,width - 1,1)
                flag_corners = 1
            else:
                self.set_value(0, width - 1,'FB')
        else:
            self.set_value(0, width - 1, 'VE')
            self.set_flag(0,width - 1,1)
            flag_corners = 1
        
        if bottom_left[0] == 'F':
            _, right_adj = self.adjacent_horizontal_values(height - 1,0)
            up_adj, _ = self.adjacent_vertical_values(height - 1,0)
            if right_adj[0] == 'F' or up_adj[0] in ['B', 'L']:
                self.set_value(height - 1, 0,'FC')
                self.set_flag(height - 1,0,1)
                flag_corners = 1
            elif up_adj[0] == 'F' or right_adj[0] in ['B', 'L']:
                self.set_value(height - 1, 0, 'FD')
                self.set_flag(height - 1,0,1)
                flag_corners = 1
            else:
                self.set_value(height - 1, 0,'FC')
        else:
            self.set_value(height - 1, 0, 'VD')
            self.set_flag(height - 1,0,1)
            flag_corners = 1
        
        if bottom_right[0] == 'F':
            left_adj, _ = self.adjacent_horizontal_values(height - 1, width - 1)
            up_adj, _ = self.adjacent_vertical_values(height - 1, width - 1)
            
            if left_adj[0] == 'F' or up_adj[0] in ['B', 'L']:
                self.set_value(height - 1, width - 1,'FC')
                self.set_flag(height - 1,width - 1,1)
                flag_corners = 1
            elif up_adj[0] == 'F' or left_adj[0] in ['B', 'L']:
                self.set_value(height - 1, width - 1, 'FE')
                self.set_flag(height - 1,width - 1,1)
                flag_corners = 1
            else:
                self.set_value(height - 1, width - 1,'FC')
        else:
            self.set_value(height - 1, width - 1, 'VC')
            self.set_flag(height - 1,width - 1,1)
            flag_corners = 1
        return self
    
    def update_adj_piece(self, row, col):
        def check_connection(value, flag, valid_values):
            if value == '555':
                return 1
            elif value[2] == '1':
                return 1 if any(value[:2] == val for val in valid_values) else 0
            else:
                return flag
    
        def set_piece_value_and_flag(piece_type, orientation):
            self.set_value(row, col, piece_type + orientation)
            self.set_flag(row, col, 1)
    
        left_val, right_val = self.adj_hori_full(row, col)
        up_val, down_val = self.adj_vert_full(row, col)
    
        flag_left = check_connection(left_val, -1, list_left)
        flag_right = check_connection(right_val, -1, list_right)
        flag_up = check_connection(up_val, -1, list_up)
        flag_down = check_connection(down_val, -1, list_down)
    
        piece_type = self.get_piece_type(row, col)
    
        if piece_type == 'V':
            if (flag_left == 0 and (flag_up == 0 or flag_down == 1)) or (flag_up == 0 and flag_right == 1) or (flag_down == 1 and flag_right == 1):
                set_piece_value_and_flag('V', 'C')
            elif (flag_left == 0 and (flag_up == 1 or flag_down == 0)) or (flag_down == 0 and flag_right == 1) or (flag_right == 1 and flag_up == 1):
                set_piece_value_and_flag('V', 'E')
            elif (flag_down == 0 and (flag_left == 1 or flag_right == 0)) or (flag_right == 0 and flag_up == 1) or (flag_left == 1 and flag_up == 1):
                set_piece_value_and_flag('V', 'B')
            elif (flag_right == 0 and (flag_up == 0 or flag_down == 1)) or (flag_up == 0 and flag_left == 1) or (flag_down == 1 and flag_left == 1):
                set_piece_value_and_flag('V', 'D')
    
        elif piece_type == 'L':
            if flag_left == 0 or flag_right == 0 or flag_down == 1 or flag_up == 1:
                set_piece_value_and_flag('L', 'H')
            elif flag_left == 1 or flag_right == 1 or flag_down == 0 or flag_up == 0:
                set_piece_value_and_flag('L', 'V')
    
        elif piece_type == 'F':
            if right_val[0] == 'F':
                flag_right = 1
            if left_val[0] == 'F':
                flag_left = 1
            if down_val[0] == 'F':
                flag_down = 1
            if up_val[0] == 'F':
                flag_up = 1
    
            if flag_left == 0 or (flag_up == 1 and flag_right == 1 and flag_down == 1):
                set_piece_value_and_flag('F', 'E')
            elif flag_right == 0 or (flag_up == 1 and flag_down == 1 and flag_left == 1):
                set_piece_value_and_flag('F', 'D')
            elif flag_down == 0 or (flag_up == 1 and flag_right == 1 and flag_left == 1):
                set_piece_value_and_flag('F', 'B')
            elif flag_up == 0 or (flag_down == 1 and flag_right == 1 and flag_left == 1):
                set_piece_value_and_flag('F', 'C')
    
        elif piece_type == 'B':
            if flag_left == 1 or (flag_up == 0 and flag_right == 0 and flag_down == 0):
                set_piece_value_and_flag('B', 'D')
            elif flag_right == 1 or (flag_up == 0 and flag_down == 0 and flag_left == 1):
                set_piece_value_and_flag('B', 'E')
            elif flag_down == 1 or (flag_up == 0 and flag_right == 0 and flag_left == 0):
                set_piece_value_and_flag('B', 'C')
            elif flag_up == 1 or (flag_down == 0 and flag_right == 0 and flag_left == 0):
                set_piece_value_and_flag('B', 'B')

    
    def inferencias(self):
        rows = len(self.rows)
        cols = len(self.rows[0])
        
        #percorrer moldura
        for col in range (1,cols - 1): # first row
            if self.get_piece_type(0, col) == 'B':
                self.set_value(0, col , 'BB')
                self.set_flag(0, col , 1)
                
            elif self.get_piece_type(0,col) == 'L':
                self.set_value(0, col , 'LH')
                self.set_flag(0, col , 1)
        
        for col in range (1, cols - 1): # last row
            if self.get_piece_type(rows - 1, col) == 'B':
                self.set_value(rows -1, col , 'BC')
                self.set_flag(rows - 1, col , 1)
                
            elif self.get_piece_type(rows - 1,col) == 'L':
                self.set_value(rows - 1, col , 'LH')
                self.set_flag(rows - 1, col , 1)
        
        for row in range (1, rows - 1): # first column
            if self.get_piece_type(row, 0) == 'B':
                self.set_value(row, 0 , 'BD')
                self.set_flag(row, 0 , 1)
                
            elif self.get_piece_type(row,0) == 'L':
                self.set_value(row, 0 , 'LV')
                self.set_flag(row, 0 , 1)
                
        for row in range (1, rows - 1): # last column
            if self.get_piece_type(row, cols -1) == 'B':
                self.set_value(row, cols -1 , 'BE')
                self.set_flag(row, cols -1 , 1)
                
            elif self.get_piece_type(row, cols-1) == 'L':
                self.set_value(row, cols -1 , 'LV')
                self.set_flag(row, cols -1 , 1)
        
        for x in range(20):   
            for row in range (rows):
                for col in range(cols):
                    if self.get_flag(row,col) == '1':
                        if self.get_flag(row, col - 1) == '0':
                            #print("Pos:", row, col -1, self.get_full_piece(row,col-1))
                            self.update_adj_piece(row, col -1)
                        if self.get_flag(row, col + 1) == '0':
                            self.update_adj_piece(row, col +1)
                        if self.get_flag(row + 1, col) == '0':
                            self.update_adj_piece(row + 1, col)
                        if self.get_flag(row - 1, col) == '0':
                            self.update_adj_piece(row - 1, col)
                
        return self

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
    
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        min_possible_actions = 4
        specific_action = []
        
        board_ = Board(np.array(state.get_board().rows)) # Convert the board to a NumPy array
        
        for row in range(len(board_.rows)):
            for col in range(len(board_.rows[0])):
                if board_.get_flag(row, col) == '0':
                    possible_actions = []
                    size = 0
                    
                    flag_left, flag_up, flag_right, flag_down = -1,-1,-1,-1
                    left_val, right_val = board_.adj_hori_full(row, col) 
                    up_val, down_val = board_.adj_vert_full(row, col)

                    if right_val == '555':
                        flag_right = 1

                    if left_val == '555':
                        flag_left = 1

                    if up_val == '555':
                        flag_up = 1

                    if down_val == '555':
                        flag_down = 1

                    if right_val[2] == '1' and flag_right != 1:
                        flag_right = 0    
                        for val in list_right:
                            if val == right_val[:2]:
                                flag_right = 1

                    if left_val[2] == '1' and flag_left != 1:
                        flag_left = 0
                        for val in list_left:
                            if val == left_val[:2]:
                                flag_left = 1

                    if up_val[2] == '1' and flag_up != 1:
                        flag_up = 0
                        for val in list_up:
                            if val == up_val[:2]:
                                flag_up = 1

                    if down_val[2] == '1' and flag_down != 1:
                        flag_down = 0
                        for val in list_down:
                            if val == down_val[:2]:
                                flag_down = 1
                    
                    if board_.get_piece_type(row, col) == 'V':
                        #print("inicio v")
                        possible_actions.append((row, col, 'VB'))
                        possible_actions.append((row, col, 'VC'))
                        possible_actions.append((row, col, 'VD'))
                        possible_actions.append((row, col, 'VE'))
                        
                        if flag_up == 1:
                            if (row, col, 'VC') in possible_actions:
                                possible_actions.remove((row, col, 'VC'))
                            if (row, col, 'VD') in possible_actions:
                                possible_actions.remove((row, col, 'VD'))

                        if flag_down == 1:
                            if (row, col, 'VB') in possible_actions:
                                possible_actions.remove((row, col, 'VB'))
                            if (row, col, 'VE') in possible_actions:
                                possible_actions.remove((row, col, 'VE'))

                        if flag_left == 1:
                            if (row, col, 'VC') in possible_actions:
                                possible_actions.remove((row, col, 'VC'))
                            if (row, col, 'VE') in possible_actions:
                                possible_actions.remove((row, col, 'VE'))

                        if flag_right == 1:
                            if (row, col, 'VB') in possible_actions:
                                possible_actions.remove((row, col, 'VB'))
                            if (row, col, 'VD') in possible_actions:
                                possible_actions.remove((row, col, 'VD'))
                                
                        if flag_up == 0:
                            if (row, col, 'VB') in possible_actions:
                                possible_actions.remove((row, col, 'VB'))
                            if (row, col, 'VE') in possible_actions:
                                possible_actions.remove((row, col, 'VE'))

                        if flag_down == 0:
                            if (row, col, 'VC') in possible_actions:
                                possible_actions.remove((row, col, 'VC'))
                            if (row, col, 'VD') in possible_actions:
                                possible_actions.remove((row, col, 'VD'))

                        if flag_left == 0:
                            if (row, col, 'VB') in possible_actions:
                                possible_actions.remove((row, col, 'VB'))
                            if (row, col, 'VD') in possible_actions:
                                possible_actions.remove((row, col, 'VD'))

                        if flag_right == 0:
                            if (row, col, 'VC') in possible_actions:
                                possible_actions.remove((row, col, 'VC'))
                            if (row, col, 'VE') in possible_actions:
                                possible_actions.remove((row, col, 'VE'))
                        
                        size = len(possible_actions)
                        if size > 1 :
                            if size < min_possible_actions:
                                min_possible_actions = size
                                specific_action = possible_actions[:]
                            #print("continue", row, col, "açoes", len(possible_actions))
                            continue
                        #print("1acao", len(possible_actions), row , col)
                        return possible_actions
                    
                    if board_.get_piece_type(row, col) == 'B':
                        
                        possible_actions.append((row, col, 'BB'))
                        possible_actions.append((row, col, 'BC'))
                        possible_actions.append((row, col, 'BD'))
                        possible_actions.append((row, col, 'BE'))
                        
                        if flag_up == 1:
                            if (row, col, 'BC') in possible_actions:
                                possible_actions.remove((row, col, 'BC'))
                            if (row, col, 'BD') in possible_actions:
                                possible_actions.remove((row, col, 'BD'))
                            if (row, col, 'BE') in possible_actions:
                                possible_actions.remove((row, col, 'BE'))

                        if flag_down == 1:
                            if (row, col, 'BB') in possible_actions:
                                possible_actions.remove((row, col, 'BB'))
                            if (row, col, 'BE') in possible_actions:
                                possible_actions.remove((row, col, 'BE'))
                            if (row, col, 'BD') in possible_actions:
                                possible_actions.remove((row, col, 'BD'))

                        if flag_left == 1:
                            if (row, col, 'BC') in possible_actions:    
                                possible_actions.remove((row, col, 'BC'))
                            if (row, col, 'BE') in possible_actions:
                                possible_actions.remove((row, col, 'BE'))
                            if (row, col, 'BB') in possible_actions:
                                possible_actions.remove((row, col, 'BB'))

                        if flag_right == 1:
                            if (row, col, 'BB') in possible_actions:
                                possible_actions.remove((row, col, 'BB'))
                            if (row, col, 'BD') in possible_actions:
                                possible_actions.remove((row, col, 'BD'))
                            if (row, col, 'BC') in possible_actions:
                                possible_actions.remove((row, col, 'BC'))
                                
                        if flag_up == 0:
                            if (row, col, 'BB') in possible_actions:
                                possible_actions.remove((row, col, 'BB'))

                        if flag_down == 0:
                            if (row, col, 'VB') in possible_actions:
                                possible_actions.remove((row, col, 'BC'))

                        if flag_left == 0:
                            if (row, col, 'BD') in possible_actions:
                                possible_actions.remove((row, col, 'BD'))

                        if flag_right == 0:
                            if (row, col, 'BE') in possible_actions:
                                possible_actions.remove((row, col, 'BE'))
                                
                        size = len(possible_actions)
                        if size > 1 :
                            if size < min_possible_actions:
                                min_possible_actions = size
                                specific_action = possible_actions[:]
                            
                            continue
                        #print("1acao", len(possible_actions), row , col , " B")
                        return possible_actions
                                
                    if board_.get_piece_type(row, col) == 'L':            
                                
                        possible_actions.append((row, col, 'LV'))
                        possible_actions.append((row, col, 'LH'))
                        
                        if flag_up == 1:
                            if (row, col, 'LV') in possible_actions:
                                possible_actions.remove((row, col, 'LV'))                            

                        if flag_down == 1:
                            if (row, col, 'LV') in possible_actions:
                                possible_actions.remove((row, col, 'LV'))
                            
                        if flag_left == 1:
                            if (row, col, 'LH') in possible_actions:
                                possible_actions.remove((row, col, 'LH'))                            

                        if flag_right == 1:
                            if (row, col, 'LH') in possible_actions:
                                possible_actions.remove((row, col, 'LH'))
                                
                        if flag_up == 0:
                            if (row, col, 'LH') in possible_actions:
                                possible_actions.remove((row, col, 'LH'))

                        if flag_down == 0:
                            if (row, col, 'LH') in possible_actions:
                                possible_actions.remove((row, col, 'LH'))

                        if flag_left == 0:
                            if (row, col, 'LV') in possible_actions:
                                possible_actions.remove((row, col, 'LV'))

                        if flag_right == 0:
                            if (row, col, 'LV') in possible_actions:
                                possible_actions.remove((row, col, 'LV'))
                                
                        size = len(possible_actions)
                        if size > 1 :
                            if size < min_possible_actions:
                                min_possible_actions = size
                                specific_action = possible_actions[:]
                            
                            continue
                        
                        #print("1acao", len(possible_actions), row , col , " L")
                        return possible_actions
                                
                    if board_.get_piece_type(row, col) == 'F':
                        
                        possible_actions.append((row, col, 'FB'))
                        possible_actions.append((row, col, 'FC'))
                        possible_actions.append((row, col, 'FD'))
                        possible_actions.append((row, col, 'FE'))
                        
                        if flag_up == 1:
                            if (row, col, 'FC') in possible_actions:
                                possible_actions.remove((row, col, 'FC'))

                        if flag_down == 1:
                            if (row, col, 'FB') in possible_actions:
                                possible_actions.remove((row, col, 'FB'))

                        if flag_left == 1:
                            if (row, col, 'FE') in possible_actions:    
                                possible_actions.remove((row, col, 'FE'))

                        if flag_right == 1:
                            if (row, col, 'FD') in possible_actions:
                                possible_actions.remove((row, col, 'FD'))
                        
                        if flag_up == 0:
                            if (row, col, 'FB') in possible_actions:
                                possible_actions.remove((row, col, 'FB'))
                            if (row, col, 'FD') in possible_actions:
                                possible_actions.remove((row, col, 'FD'))
                            if (row, col, 'FE') in possible_actions:
                                possible_actions.remove((row, col, 'FE'))

                        if flag_down == 0:
                            if (row, col, 'FC') in possible_actions:
                                possible_actions.remove((row, col, 'FC'))
                            if (row, col, 'FD') in possible_actions:
                                possible_actions.remove((row, col, 'FD'))
                            if (row, col, 'FE') in possible_actions:
                                possible_actions.remove((row, col, 'FE'))

                        if flag_left == 0:
                            if (row, col, 'FC') in possible_actions:    
                                possible_actions.remove((row, col, 'FC'))
                            if (row, col, 'FB') in possible_actions:
                                possible_actions.remove((row, col, 'FB'))
                            if (row, col, 'FD') in possible_actions:
                                possible_actions.remove((row, col, 'FD'))

                        if flag_right == 0:
                            if (row, col, 'FB') in possible_actions:
                                possible_actions.remove((row, col, 'FB'))
                            if (row, col, 'FE') in possible_actions:
                                possible_actions.remove((row, col, 'FE'))
                            if (row, col, 'FC') in possible_actions:
                                possible_actions.remove((row, col, 'FC'))
                        
                        #print(possible_actions,'\n')
                        
                        size = len(possible_actions)
                        if size > 1 :
                            if size < min_possible_actions:
                                min_possible_actions = size
                                specific_action = possible_actions[:]
                                #print("specific,", specific_action)
                            continue
                        #print("1acao", len(possible_actions), row , col)        
                        return possible_actions
                    
        #print("aqui", len(specific_action))
        return specific_action
        
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        row, col, rotated_piece = action
        
         # Create a copy of the current board using np.copy
        current_board = state.get_board()
        new_board = np.copy(current_board.rows)
    
        # Update the piece at the specified coordinates with the rotated piece
        new_value = rotated_piece + '1'
        new_board[row][col] = new_value
        
        # Create a new Board object with the updated rows
        new_board_instance = Board(new_board)
    
        # Create a new PipeManiaState object with the updated board
        new_state = PipeManiaState(new_board_instance)
        
        #print('RESULT')
        #print(new_state)
        #print('\n')
        
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #board = Board(state.get_board())
        board = Board(np.array(state.get_board().rows))
        board_size = len(board.rows)
        #print('GOAL TEST')
        #print(board)
        #print('\n')
        # Iterate over the board to check if all pipes are connected
        count = 0
        stack = [(0,0)]
        visited = create_zero_initialized_board(board_size, board_size)
        
        while stack:
            piece = stack.pop()
            
            row, col = piece
            
            if visited[row][col] == 1:
                continue
            
            visited[row][col] = 1
            
            left_val, right_val = board.adjacent_horizontal_values(row,col)
            up_val, down_val = board.adjacent_vertical_values(row, col)
            
            if col + 1 < board_size and visited[row][col + 1] == 0:
                stack.append((row, col + 1))
            if col - 1 >= 0 and visited[row][col - 1] == 0:
                stack.append((row, col - 1))
            if row + 1 < board_size and visited[row + 1][col] == 0:
                stack.append((row + 1, col))
            if row - 1 >= 0 and visited[row - 1][col] == 0:
                stack.append((row - 1, col))
            
            if  board.get_piece_type(row,col) == 'F': 
                if board.get_piece_orien(row,col) == 'C':
                    if up_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:                                
                            return False
                        
                elif  board.get_piece_orien(row,col) == 'D':
                    if right_val == None:
                        return False
                    for val in list_right:
                        if val == right_val: 
                            return False
                        
                elif board.get_piece_orien(row,col) == 'B':
                    if down_val == None:
                        return False
                    for val in list_down:
                        if val == down_val:
                            return False
                        
                elif board.get_piece_orien(row,col) == 'E':
                    if left_val == None:
                        return False
                    for val in list_left:
                        if val == left_val:
                            return False
                        
            elif board.get_piece_type(row,col) == 'B':
                if board.get_piece_orien(row,col) == 'C':
                    if left_val == None or up_val == None or right_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:
                            return False
                    for val in list_left:
                        if val == left_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
                        
                elif board.get_piece_orien(row,col) == 'D':
                    if down_val == None or up_val == None or right_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:
                            return False
                    for val in list_down:
                        if val == down_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
                        
                elif board.get_piece_orien(row,col) == 'B':
                    
                    if down_val == None or left_val == None or right_val == None:
                        return False
                    for val in list_down:
                        if val == down_val:
                            return False
                    for val in list_left:
                        if val == left_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
            
                elif board.get_piece_orien(row,col) == 'E':
                    
                    if down_val == None or up_val == None or left_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:
                            return False
                    for val in list_left:
                        if val == left_val:
                            return False
                    for val in list_down:
                        if val == down_val:
                            return False
                        
            elif board.get_piece_type(row,col) == 'V':
                if board.get_piece_orien(row,col) == 'C':
                    
                    if left_val == None or up_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:
                            return False
                    for val in list_left:
                        if val == left_val:
                            return False
                        
                elif board.get_piece_orien(row,col) == 'D':
                    
                    if right_val == None or up_val == None:
                        return False
                    for val in list_up:
                        if val == up_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
                        
                elif board.get_piece_orien(row,col) == 'B':
                     
                    if right_val == None or down_val == None:
                        return False
                    for val in list_down:
                        if val == down_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
                    
                elif board.get_piece_orien(row,col) == 'E':
                    
                    if left_val == None or down_val == None:
                        return False
                    for val in list_down:
                        if val == down_val:
                            return False
                    for val in list_left:
                        if val == left_val:
                            return False
                        
            elif board.get_piece_type(row,col) == 'L':
                    
                if board.get_piece_orien(row,col) == 'H':
                    
                    if left_val == None or right_val == None:
                        return False
                    for val in list_left:
                        if val == left_val:
                            return False
                    for val in list_right:
                        if val == right_val:
                            return False
                    
                elif board.get_piece_orien(row,col) == 'V':
                                           
                    if up_val == None or down_val == None:
                        return False
                    for val in list_down:
                        if val == down_val:
                            return False
                    for val in list_up:
                        if val == up_val:
                            return False
            
            count +=1
                    
        if count == (board_size * board_size):
            return True

    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    board_instance = Board.parse_instance()
    corners_instance = Board.corners(board_instance)
    infererencias_instance = Board.inferencias(corners_instance)    
    problem = PipeMania(infererencias_instance)
    goal_node: Node = depth_first_tree_search(problem)
    print(goal_node.state)
 
    pass 
