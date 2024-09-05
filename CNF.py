class CNF:
    def __init__(self, number_of_variables, number_of_clauses, clauses):
        self.number_of_variables = number_of_variables
        self.number_of_clauses = number_of_clauses
        self.clauses = clauses

    def __str__(self) -> str:
        name = "c Staircase at least one"
        head = "p cnf " + str(self.number_of_variables) + " " + str(self.number_of_clauses)
        variables_list = ""
        for i in range(1, self.number_of_variables + 1):
            variables_list += str(i) + " "
        variables_list += "0"

        clauses_list = ""

        for clause in self.clauses:
            clause_str = ""
            for variable in clause:
                clause_str += str(variable) + " "
            clause_str += "0"
            clauses_list += clause_str + "\n"

        res = name + "\n" + head + "\n" + clauses_list

        return res

    def write_to_file(self, file_name):
        f = open(file_name, "w")
        f.write(self.__str__())
        f.close()

    def append_cnf(self, clause):
        self.clauses.append(clause)
        self.number_of_clauses += 1
