import math


class StairCaseEncoding:
    def __init__(self, n, k, variable_list, current_variable_count):
        self.n = n
        self.k = k
        self.variable_list = variable_list
        self.variable_count = 0
        self.current_variable_count = current_variable_count
        self.clause_count = 0
        self.cnf = []
        self.number_of_windows = math.ceil(n / k)
        self.x_map = {}
        self.l_map = {}
        self.r_map = {}
        self.add_x_map()
        self.add_l_map()
        if self.n > k:
            self.add_r_map()
        #self.building_l()

        self.building_r()

    def __str__(self) -> str:
        x_str: str = self.x_map.__str__()
        l_str: str = self.l_map.__str__()
        r_str: str = self.r_map.__str__()
        cnf_str: str = self.cnf.__str__()
        res = "X Map: " + x_str + "\n" + "L MAP: " + l_str + "\n" + "R Map: " + r_str + "\n" + "CNF: " + cnf_str
        return res

    def add_x_map(self):
        j = 0
        for i in range(1, self.n + 1):
            self.x_map[i] = self.variable_list[j]
            j += 1

    def add_l_map(self):
        number_of_l = self.n
        if self.number_of_windows % 2 != 0 and self.n % self.k == 0:
            number_of_l = number_of_l - self.k
        for i in range(1, number_of_l + 1):
            print("i: ", i)
            if i % self.k == 0:
                self.l_map[i] = self.x_map[i]
            else:
                self.current_variable_count += 1
                self.l_map[i] = self.current_variable_count

        if (self.number_of_windows % 2 == 0) and (self.n % self.k != 0):
            self.current_variable_count -= 1
            self.l_map[self.n] = self.x_map[self.n]

    def add_r_map(self):
        for i in range(1, self.n - self.k + 1):
            if i % self.k == 1:
                self.r_map[i] = self.l_map[i]
            elif i % self.k == 2:
                self.r_map[i] = self.x_map[i + self.k - 1]
            else:
                self.current_variable_count += 1
                self.r_map[i] = self.current_variable_count

    def building_l(self):
        number_of_left_blocks = self.number_of_windows
        if self.number_of_windows % 2 != 0:
            number_of_left_blocks -= 1

        for i in range(0, number_of_left_blocks):
            left_index = i * self.k + 1
            right_index = left_index + self.k - 1
            self.building_l_block(left_index, right_index)

    def building_l_block(self, left_index, right_index):
        if left_index < 1:
            return
        if left_index > right_index:
            return

        if right_index > self.n:
            right_index = self.n - 1

        print("left index: ", left_index, " ", "right index: ", right_index)
        for i in range(right_index, left_index, -1):
            print("i: ", i)
            cnf_line = [-self.l_map[i], self.l_map[i - 1]]
            self.cnf.append(cnf_line)
            cnf_line = [-self.x_map[i], self.l_map[i - 1]]
            self.cnf.append(cnf_line)

    def building_r(self):
        number_of_r_block = self.number_of_windows - 1
        for i in range(1, number_of_r_block + 1):
            left_index = i * self.k + 1
            right_index = left_index + self.k - 1
            print("left index: ", left_index, " ", "right index: ", right_index)
            # self.building_r_block(left_index, right_index)

    def building_r_block(self, left_index, right_index):


        for i in range(left_index + 1, right_index + 1):
            cnf_line = [-self.r_map[i-1], self.r_map[i]]
            self.cnf.append(cnf_line)
            x_index = (i - 1) + (math.ceil(i / self.k) - 1) * self.k
            print("i: ", i, "-","x index: ", x_index)
            # cnf_line = [-self.x_map[x_index], self.r_map[i]]
            # self.cnf.append(cnf_line)



