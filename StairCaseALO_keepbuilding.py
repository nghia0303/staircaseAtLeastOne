# With missing block, keep building until full block
# The number of row wil be (n)

import math

from CNF import CNF

class StairCaseALO:

    def __init__(self, n, k, variable_list, current_variable_count):
        self.n = n
        self.k = k
        self.variable_list = variable_list
        self.variable_count = 0
        self.current_variable_count = current_variable_count
        self.clause_count = 0
        self.cnf = []
        self.number_of_windows = math.ceil(n / k)
        self.number_of_rows = n - k + 1
        self.x_map = {}
        self.l_map = {}
        self.r_map = {}
        self.number_of_l_variables = 0
        self.number_of_r_variables = 0
        self.add_x_map()
        # self.number_of_l_variables = 0
        # self.number_of_
        self.add_l_map()
        if self.n > k:
            self.add_r_map()
        self.building_l()

        self.building_r()

        self.building_staircase_rows()

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

    # Added variable id to l_map (without the last block)
    def add_l_map(self):

        number_of_l_row = self.number_of_rows
        if self.n % self.k != 0:
            number_of_l_row = self.n - 1
            self.l_map[self.n] = self.x_map[self.n]
        for i in range(1, number_of_l_row + 1):
            if i % self.k == 0:
                self.l_map[i] = self.x_map[i]
            elif i % self.k != 1:
                self.current_variable_count += 1
                self.l_map[i] = self.current_variable_count
                self.number_of_l_variables += 1

    # Added variable id to r_map (without the last block)
    def add_r_map(self):
        for i in range(1, self.number_of_rows + 1):
            if i % self.k == 1:
                # self.r_map[i] = self.l_map[i]
                pass
            elif i % self.k == 2:
                self.r_map[i] = self.x_map[i + self.k - 1]
            else:
                self.current_variable_count += 1
                self.r_map[i] = self.current_variable_count

    # Building constraints for l_block (without last block)
    # L(i) + X(i-1) -> L(i-1)
    # <=> (-L(i) + L(i-1)) ^ (-X(i-1) + L(i-1))
    def building_l(self):
        print("Building l_map: --------------------------------------")
        number_of_l_block = math.ceil(self.number_of_rows / self.k)
        if self.n % self.k == 0:
            number_of_l_block -= 1
        for i in range(0, number_of_l_block):
            left_index = i * self.k + 1
            right_index = left_index + self.k - 1
            print("left_index: ", left_index, " ", "right_index: ", right_index)
            self.building_l_block(left_index, right_index)


    def building_l_block(self, left_index, right_index):
        if right_index > self.n:
            right_index = self.n
        for i in range(right_index, left_index + 1, -1):
            print("i: ", i)
            cnf_line = [-self.l_map[i], self.l_map[i - 1]]
            print("-L", i, " ", "L", i - 1, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

            cnf_line = [-self.x_map[i-1], self.l_map[i - 1]]
            print("-X", i-1, " ", "L", i - 1, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

            cnf_line = [-self.l_map[i-1], self.l_map[i], self.x_map[i-1]]
            print("-L", i-1, " ", "L", i, " ", "X", i-1, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

    # Building constraints for r_block (without last block)
    # R(i - 1) + X( (i - 1) + (ceil(i / k) - 1) * k ) -> Ri
    def building_r(self):
        print("Building r_map: --------------------------------------")
        number_of_r_block = self.number_of_windows - 1
        for i in range(0, number_of_r_block):
            left_index = i * self.k + 2
            right_index = left_index + self.k - 1
            print("left_index: ", left_index, " ", "right_index: ", right_index)
            self.building_r_block(left_index, right_index)


    def building_r_block(self, left_index, right_index):
        if right_index > self.number_of_rows:
            right_index = self.number_of_rows
        for i in range(left_index + 1, right_index):
            print("i: ", i)
            cnf_line = [-self.r_map[i-1], self.r_map[i]]
            print("-R", i-1, " ", "R", i, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

            x_index = self.k + i - 1
            cnf_line = [-self.x_map[x_index], self.r_map[i]]
            print("-X", x_index, " ", "R", i, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

            cnf_line = [-self.r_map[i], self.r_map[i-1], self.x_map[x_index]]
            print("-R", i, " ", "R", i-1, " ", "X", x_index, " ", cnf_line)
            self.cnf.append(cnf_line)
            self.clause_count += 1

    def building_staircase_rows(self):
        print("Building staircase rows: --------------------------------------", self.number_of_rows)
        for i in range(1, self.number_of_rows + 1):
            if i % self.k != 1:
                cnf_line = [self.l_map[i], self.r_map[i]]
                self.cnf.append(cnf_line)
                self.clause_count += 1
                print("L", i, " ", "R", i, " ", cnf_line)
            else:
                # cnf_line = [self.l_map[i]]
                # if i != self.number_of_rows:
                #     cnf_line = [self.x_map[i], self.l_map[i+1]]
                #     print("X", i, " ", "L", i+1)
                #     self.cnf.append(cnf_line)
                #     self.clause_count += 1
                # else:
                #     cnf_line = [self.x_map[i], self.r_map[i-1]]
                #     print("X", i, " ", "R", i - 1)
                #     self.cnf.append(cnf_line)
                #     self.clause_count += 1

                cnf_line = [self.x_map[i]]
                print("X", i, end=" ")
                if (i + 1) in self.l_map:
                    cnf_line.append(self.l_map[i + 1])
                    print("L", i + 1, end=" ")
                if (i - 1) in self.r_map:
                    cnf_line.append(self.r_map[i - 1])
                    print("R", i - 1, end=" ")
                print()
                self.cnf.append(cnf_line)
                self.clause_count += 1







def main():

    n = 18
    k = 5
    variable_list = list(range(1, n+1))

    encoding = StairCaseALO(
        n, k, variable_list, n
    )

    new_number_of_variables = encoding.current_variable_count
    new_number_of_clauses = encoding.clause_count
    cnf = CNF(
        new_number_of_variables,
        new_number_of_clauses,
        encoding.cnf
    )
    print(encoding)
    print("added variable", encoding.current_variable_count)
    print("added clauses", encoding.clause_count)
    cnf.write_to_file("cnf/StairCaseALO_keepBuilding.cnf")
if __name__ == "__main__":
    main()
