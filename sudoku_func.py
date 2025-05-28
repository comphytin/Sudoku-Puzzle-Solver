class SudokuFunctions:
    
    def __init__(self, digits_matrix):
        self.digits_matrix = digits_matrix

    def miniSquare(self, spot):
        mini_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                mini_list[i][j] = self.digits_matrix[(spot - 1) / 3 * 3 + i][(spot - 1) % 3 * 3 + j]
    
    def isSolved(self):

        pass

    def find_solution(self):
        pass