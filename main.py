class Node:
    def __init__(self, pos):
        self.num = None
        self.pos = pos

        self.row_adj = set()
        self.col_adj = set()
        self.group_adj = set()
        self.adjecent = set()

        self.possibliities = set(range(1,10))

class Board:
    def __init__(self):
        nodes = [[Node((x,y)) for x in range(9)] for y in range(9)]
        for x in range(9):
            for y in range(9):
                x_base = x // 3
                y_base = y // 3
                # Group
                for i in range(3):
                    for j in range(3):
                        nodes[x][y].group_adj.add(nodes[x_base*3+i][y_base*3+j])

                for i in range(9):
                    nodes[x][y].col_adj.add(nodes[x][i])
                    nodes[x][y].row_adj.add(nodes[i][y])

                nodes[x][y].group_adj.remove(nodes[x][y])
                nodes[x][y].col_adj.remove(nodes[x][y])
                nodes[x][y].row_adj.remove(nodes[x][y])
                nodes[x][y].adjecent = nodes[x][y].group_adj | nodes[x][y].col_adj | nodes[x][y].row_adj
        self.nodes = nodes

    def merge_from_file(self, file_name):
        with open(file_name) as f:
            for y, line in enumerate(f):
                for x, num in enumerate(line.strip()):
                    if num != '*':
                        self.nodes[x][y].num = int(num)
                        self.nodes[x][y].possibliities = set()
        self._update_possiblities()

    def display(self):
        for y in range(9):
            if(y % 3 == 0):
                print('- - - - - - - - - - -')
            for x in range(9):
                if(x % 3 == 0):
                    print('|', end='')
                if self.nodes[x][y].num is None:
                    print('*', end=' ')
                else:
                    print(self.nodes[x][y].num, end=' ')
            print()

    def _update_possiblities(self):
        for x in range(9):
            for y in range(9):
                if self.nodes[x][y].num is not None:
                    continue
                for adj_node in self.nodes[x][y].adjecent:
                    if adj_node.num is not None:
                        self.nodes[x][y].possibliities-={adj_node.num}

    def solve_a(self):
        flag = False
        for x in range(9):
            for y in range(9):
                if self.nodes[x][y].num is None and len(self.nodes[x][y].possibliities) == 1:
                    self.nodes[x][y].num = self.nodes[x][y].possibliities.pop()
                    flag = True
        return flag
            
    def solve_b(self):
        flag = False
        for x in range(9):
            for y in range(9):            
                if self.nodes[x][y].num is None:
                    row_p = set()
                    col_p = set()
                    group_p = set()

                    for adj_node in self.nodes[x][y].row_adj:
                        if adj_node.num is None:
                            row_p |= adj_node.possibliities
                    for adj_node in self.nodes[x][y].col_adj:
                        if adj_node.num is None:
                            col_p |= adj_node.possibliities
                    for adj_node in self.nodes[x][y].group_adj:
                        if adj_node.num is None:
                            group_p |= adj_node.possibliities

                    # print(f"{adj_possibilities=}")
                    p_from_row = (set(range(1,10)) - row_p) & self.nodes[x][y].possibliities
                    p_from_col = (set(range(1,10)) - col_p) & self.nodes[x][y].possibliities
                    p_from_group = (set(range(1,10)) - group_p) & self.nodes[x][y].possibliities


                    # print(f"{self.nodes[x][y].possibliities=}")
                    # print(intersection)
                    if(len(p_from_row) == 1 or len(p_from_col) == 1 or len(p_from_group) == 1):
                        if(len(p_from_row) == 1):
                            self.nodes[x][y].num = p_from_row.pop()
                        elif(len(p_from_col) == 1):
                            self.nodes[x][y].num = p_from_col.pop()
                        elif(len(p_from_group) == 1):
                            self.nodes[x][y].num = p_from_group.pop()

                        self._update_possiblities()
                        flag = True
        return flag
                    
        

    def solve(self):
        for time in range(1000):
            flag_a = self.solve_a()
            self._update_possiblities()
            flag_b = self.solve_b()
            self._update_possiblities()
            if(not (flag_a or flag_b)):
                print(f"No more solution {time=}")
                break


if __name__ == "__main__":
    board = Board()
    board.merge_from_file('board1.txt')

    print("Before solve:")
    board.display()

    board.solve()

    print("After solve:")
    board.display()