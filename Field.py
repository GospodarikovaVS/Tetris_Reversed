import random
from PyQt5.QtWidgets import QFrame


class Field(QFrame):


    def __init__(self, parent, row, col, dif):
        super().__init__(parent)

        self.init_field(row, col, dif)

    def init_field(self, row, col, dif):
        self.BlockHeight = row
        self.BlockWidth = col
        self.Difficulty = dif
        self.shadow_field = []
        self.field = []
        self.cur_loc = self.BlockWidth//2
        self.cur_blocks = [0]
        self.new_fields()


    def start(self):
        self.cur_loc = self.BlockWidth // 2
        self.cur_blocks = [0]
        self.refresh_fields()
        self.field[self.BlockHeight - 1][self.cur_loc] = 8

    def new_fields(self):
        for row in range(3):
            self.field.append([])
            self.shadow_field.append([])
            for col in range(self.BlockWidth):
                if random.randint(1, 100) < self.Difficulty:
                    self.field[row].append(6)
                elif random.randint(1, 100) < self.Difficulty*0.5:
                    self.field[row].append(7)
                else:
                    self.field[row].append(random.randint(1, 5))
                self.shadow_field[row].append(0)
        for row in range(3, self.BlockHeight):
            self.field.append([])
            self.shadow_field.append([])
            for col in range(self.BlockWidth):
                self.field[row].append(0)
                self.shadow_field[row].append(0)

    def refresh_fields(self):
        for row in range(3):
            for col in range(self.BlockWidth):
                if random.randint(1, 100) < self.Difficulty:
                    self.field[row][col] = 6
                elif random.randint(1, 100) < self.Difficulty*0.5:
                    self.field[row][col] = 7
                else:
                    self.field[row][col] = random.randint(1, 5)
                self.shadow_field[row][col] = 0
        for row in range(3, self.BlockHeight):
            for col in range(self.BlockWidth):
                self.field[row][col] = 0
                self.shadow_field[row][col] = 0

    def move(self, shift):
        next_loc = self.cur_loc + shift
        if 0 <= next_loc < self.BlockWidth:
            if self.field[self.BlockHeight - 1 - len(self.cur_blocks)][next_loc] == 0:
                self.field[self.BlockHeight - 1][next_loc] = self.field[self.BlockHeight - 1][self.cur_loc]
                self.field[self.BlockHeight - 1][self.cur_loc] = 0
                for i in range(len(self.cur_blocks)):
                    self.field[self.BlockHeight - 2 - i][next_loc] = self.field[self.BlockHeight - 2 - i][self.cur_loc]
                    self.field[self.BlockHeight - 2 - i][self.cur_loc] = 0
                self.cur_loc = next_loc

    def action(self):
        count = 0
        if self.cur_blocks[0] == 0:
            self.drop()
        else:
            count = self.up()
        return count

    def drop(self):
        i = self.BlockHeight - 2
        while self.field[i][self.cur_loc] == 0:
            i -= 1
        if not self.field[i][self.cur_loc] == 7:
            self.cur_blocks[0] = self.field[i][self.cur_loc]
            self.field[i][self.cur_loc] = 0
            while i-1 >= 0 and self.field[i-1][self.cur_loc] == self.cur_blocks[0]:
                i -= 1
                self.cur_blocks.append(self.field[i][self.cur_loc])
                self.field[i][self.cur_loc] = 0
            for j in range(len(self.cur_blocks)):
                self.field[self.BlockHeight - 2 - j][self.cur_loc] = self.cur_blocks[j]

    def up(self):
        count = 0
        i = self.BlockHeight - 2 - len(self.cur_blocks)
        while i > -1 and self.field[i][self.cur_loc] == 0:
            i -= 1
        i += 1
        if self.cur_blocks[0] == 6:
            count += self.destroy_whole_col()
            self.field[self.BlockHeight - 2][self.cur_loc] = 0
        else:
            for j in range(len(self.cur_blocks)):
                self.field[i + j][self.cur_loc] = self.cur_blocks[0]
                self.field[self.BlockHeight - 2 - j][self.cur_loc] = 0
            count += self.check_for_equivalent_blocks(i)
        self.cur_blocks = [0]
        return count

    def destroy_whole_col(self):
        count = 0
        col = self.cur_loc
        for row in range(self.BlockHeight - 2):
            if not self.field[row][col] == 0:
                count += 1
                self.field[row][col] = 0
        return count

    def check_for_equivalent_blocks(self, i):
        count = self.recursion(i, self.cur_loc, self.field[i][self.cur_loc])
        if count > 3:
            self.delete_with_shadow()
            self.deleter_space()
            return count
        self.refresh_shadow()
        return 0

    def recursion(self, row, col, type):
        count = 0
        self.shadow_field[row][col] = 1
        if row - 1 >= 0 and self.shadow_field[row-1][col] == 0 and self.field[row-1][col] == type:
            count += self.recursion(row-1, col, type)
        if row + 1 <= self.BlockHeight - 3 and self.shadow_field[row+1][col] == 0 and self.field[row+1][col] == type:
            count += self.recursion(row+1, col, type)
        if col - 1 >= 0 and self.shadow_field[row][col-1] == 0 and self.field[row][col-1] == type:
            count += self.recursion(row, col-1, type)
        if col + 1 < self.BlockWidth and self.shadow_field[row][col+1] == 0 and self.field[row][col+1] == type:
            count += self.recursion(row, col+1, type)
        return count+1

    def delete_with_shadow(self):
        for row in range(self.BlockHeight):
            for col in range(self.BlockWidth):
                if not self.shadow_field[row][col] == 0:
                    self.field[row][col] = 0

    def deleter_space(self):
        for col in range(self.BlockWidth):
            i = self.BlockHeight - 3
            while i > 0 and self.field[i][col] == 0:
                i -= 1;
            for row in range(i):
                while self.field[row][col] == 0:
                    self.del_space(row, col, i)

    def del_space(self, row_space, col, i):
        for row in range(row_space, i):
            self.field[row][col] = self.field[row+1][col]
        self.field[i][col] = 0

    def refresh_shadow(self):
        for row in range(self.BlockHeight):
            for col in range(self.BlockWidth):
                self.shadow_field[row][col] = 0

    def one_line_down(self):
        for row in range(self.BlockHeight-3, 0, -1):  # идти наоборот - вверх
            self.field.append([])
            for col in range(self.BlockWidth):
                self.field[row][col] = self.field[row-1][col]
        for j in range(len(self.cur_blocks)):
            self.field[self.BlockHeight - 2 - j][self.cur_loc] = self.cur_blocks[0]

        for col in range(self.BlockWidth):
            if random.randint(1, 100) < self.Difficulty:
                self.field[0][col] = 6
            elif random.randint(1, 100) < self.Difficulty * 0.5:
                self.field[0][col] = 7
            else:
                self.field[0][col] = random.randint(1, 5)

    def check_for_game_over(self):
        for col in range(self.BlockWidth):
            if self.field[self.BlockHeight-3][col] != 0:
                if len(self.cur_blocks) < 2 or self.cur_loc != col:
                    return True
        return False
