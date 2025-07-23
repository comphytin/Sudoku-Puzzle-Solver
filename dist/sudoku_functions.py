class SudokuFunctions:

    def __init__(self, sudokuBoard):
        self.sudokuBoard = sudokuBoard

    def isValid(self):
        setRowColumn = set()
        setMiniSquare = set()
        for i in range(9):
            for j in range(9):
                if self.sudokuBoard[i][j].text in setRowColumn and self.sudokuBoard[i][j].text != "0":
                    return False
                else:
                    setRowColumn.add(self.sudokuBoard[i][j].text)
            setRowColumn.clear()

            for j in range(9):
                if self.sudokuBoard[j][i].text in setRowColumn and self.sudokuBoard[j][i].text != "0":
                    return False
                elif self.sudokuBoard[j][i].text != "0":
                    setRowColumn.add(self.sudokuBoard[j][i].text)

            setRowColumn.clear()

        for i in range(9):
            arr2D = self.miniSquare(i)
            for j in range(3):
                for k in range(3):
                    if arr2D[j][k] in setMiniSquare and arr2D[j][k] != "0":
                        return False
                    else:
                        setMiniSquare.add(arr2D[j][k])
            setMiniSquare.clear()
        return True

    def miniSquare(self, spot):
        mini = [
            ["0", "0", "0"],
            ["0", "0", "0"],
            ["0", "0", "0"]
        ]
        for r in range(3):
            for c in range(3):
                mini[r][c] = self.sudokuBoard[(spot - 1) // 3 * 3 + r][(spot - 1) % 3 * 3 + c].text
        
        return mini

    def isSolved(self):
        if self.isValid() == True:
            for i in range(9):
                for j in range(9):
                    if self.sudokuBoard[i][j].text == "" or self.sudokuBoard[i][j].text == "0":
                        return False
            rowMap = {}
            columnMap = {}
            miniSquareMap = {}
            for i in range(9):
                for j in range(9):
                    if self.sudokuBoard[i][j].text in rowMap and not self.validNum(int(self.sudokuBoard[i][j].text)):
                        return False
                    else:
                        rowMap.update({self.sudokuBoard[i][j].text: 1})
                for j in range(9):
                    if self.sudokuBoard[j][i].text in columnMap and not self.validNum(int(self.sudokuBoard[j][i].text)):
                        return False
                    else:
                        rowMap.update({self.sudokuBoard[j][i].text: 1})
                rowMap.clear()
                columnMap.clear()
            
            for i in range(1, 10):
                arr2D = self.miniSquare(i)
                for j in range(3):
                    for k in range(3):
                        if arr2D[j][k] in miniSquareMap:
                            return False
                        else:
                            miniSquareMap.update({arr2D[j][k]: 1})
                miniSquareMap.clear()
            return True
        
        return False
    
    def validNum(self, num):
        return num >= 1 and num <= 9
    
    def numCheck(self, num, rowIndex, colIndex):
        for i in range(9):
            if self.sudokuBoard[rowIndex][i].text == str(num) or self.sudokuBoard[i][colIndex].text == str(num):
                return False
            rowCheck = rowIndex // 3 * 3
            columnCheck = colIndex // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.sudokuBoard[rowCheck + i][columnCheck + j].text == str(num):
                    return False
        return True

    def solve(self):
        if self.isValid() and self.isSolved():
            return True
        for i in range(9):
            for j in range(9):
                if self.sudokuBoard[i][j].text == str(0) or self.sudokuBoard[i][j].text == "":
                    for digit in range(1, 10):
                        if self.numCheck(digit, i, j):
                            self.sudokuBoard[i][j].change_text(str(digit), (0, 0, 255))
                            if self.solve():
                                return True
                            self.sudokuBoard[i][j].text = "0"
                    return False
        return True
