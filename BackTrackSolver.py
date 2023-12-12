import time
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class BackTrackSolver:
    def __init__(self, data_table):
        self.variables = {}
        self.constraints = []
        self.unassigned_var = []
        self.data_table = data_table
        self.var_constraint = {}

    def add_variable(self, variable, domain):
        self.variables[tuple(variable)] = domain.copy()
        self.unassigned_var.append(tuple(variable))

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def solve(self):
        solutions = []
        self.backtrack({}, solutions)
        return solutions

    def is_consistent(self, assignment):
        constraint_function = self.BT_constraint
        for constraint in self.constraints:
            variables = constraint
            if not constraint_function(*variables):
                return False
        return True

    def MCV(self):
        var = self.unassigned_var[-1]
        domain_len = len(self.variables[var])
        for v in self.unassigned_var:
            if len(self.variables[v]) < domain_len:
                var = v
                domain_len = len(self.variables[v])
        return var

    def BT_constraint(self, variables, target_sum):
        assigned_values = [self.data_table[var[0]][var[1]] for var in variables if
                           self.data_table[var[0]][var[1]] != 0]
        # print("BTK", variables, assigned_values, target_sum)

        if len(assigned_values) != len(set(assigned_values)):
            # print("tekrari")
            return False

        unassigned_variable_cnt = len(variables) - len(assigned_values)
        assigned_sum = sum(assigned_values)

        cnt = unassigned_variable_cnt
        max_remain_value = sum(i for i in range(9, 1, -1) if i not in assigned_values and (cnt := cnt - 1) >= 0)

        cnt = unassigned_variable_cnt
        min_remain_value = sum(i for i in range(1, 10) if i not in assigned_values and (cnt := cnt - 1) > 0)

        if target_sum - assigned_sum > max_remain_value:
            return False
        if target_sum - assigned_sum < min_remain_value:
            return False
        if len(assigned_values) == len(variables) and sum(assigned_values) != target_sum:
            return False
        return True

    def is_consistent_var(self, var):
        # print("var constraint ", var, self.var_constraint[var])
        constraint_function = self.BT_constraint
        for i in self.var_constraint[var]:
            constraint = self.constraints[i]
            variables = constraint
            if not constraint_function(*variables):
                return False
        return True

    def filter_from_neighbors(self, value, var):
        # print("var, value", var, value)
        for constraint_ind in self.var_constraint[var]:
            # print("constraint_ind", constraint_ind)
            constraint_var, constraint_sum = self.constraints[constraint_ind][0], self.constraints[constraint_ind][1]
            for v in constraint_var:
                if v == var:
                    continue
                # print("remove variable domain type: ", v, self.variables[tuple(v)])
                try:
                    self.variables[tuple(v)].remove(value)
                    # print("v :", self.variables[tuple(v)])
                except:
                    pass

    def add_to_neighbors(self, value, var):
        for constraint_ind in self.var_constraint[var]:
            constraint_var, constraint_sum = self.constraints[constraint_ind][0], self.constraints[constraint_ind][1]
            for v in constraint_var:
                if v == var:
                    continue
                # print("add variable domain type: ", self.variables[tuple(v)])
                if value not in self.variables[tuple(v)]:
                    self.variables[tuple(v)].append(value)
                    # print("v :", self.variables[tuple(v)])

    def backtrack(self, assignment, solutions):
        if len(assignment) == len(self.variables):
            solutions.append(assignment.copy())
            return
        #var = self.unassigned_var[-1]
        var = self.MCV()
        self.unassigned_var.remove(var)

        domain = self.variables[var].copy()
        for value in domain:
            assignment[var] = value
            # print("assigned variable:", len(assignment), len(self.variables))
            self.data_table[var[0]][var[1]] = value
            self.filter_from_neighbors(value, var)
            if self.is_consistent_var(var):
                self.backtrack(assignment, solutions)
                if len(solutions) == len(self.variables):
                    break
            self.data_table[var[0]][var[1]] = 0
            self.add_to_neighbors(value, var)
            assignment.pop(var)
        self.unassigned_var.append(var)