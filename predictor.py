class Predictor:

    predict = lambda: None
    btb = [0] * 1024
    bht = [[0 for x in range(6)] for y in range(1024)]
    correct = 0
    incorrect = 0
    branches = []

    def __init__(self, method):
        if method == 'taken':
            self.predict = self.taken
        if method == 'not_taken':
            self.predict = self.not_taken
        elif method == 'two_bit':
            self.predict = self.two_bit

    def taken(self, pc, instruction):
        opcode = instruction[: instruction.find(' ')]
        if opcode == 'j':
            return int(instruction.split(' ')[1:][0])
        if opcode == 'beq' or opcode == 'bne' or opcode == 'ble' or opcode == 'blt':
            return int(instruction.split(' ')[1:][2])
        return pc + 1

    def not_taken(self, pc, instruction):
        opcode = instruction[: instruction.find(' ')]
        if opcode == 'j':
            return int(instruction.split(' ')[1:][0])
        return pc + 1

    def two_bit(self, pc, instruction):
        opcode = instruction[: instruction.find(' ')]
        if opcode == 'j':
            return int(instruction.split(' ')[1:][0])
        index = self.bht[pc][0] * 2 + self.bht[pc][1] + 2
        if self.bht[pc][index] > 1:
            return self.btb[pc]
        else:
            return pc + 1

    def check(self, rf, op, operands, pc, next_pc, executed):
        correct_pc = next_pc
        taken = False
        if op == 'beq':
            if rf[int(operands[0][1:])] == rf[int(operands[1][1:])]:
                correct_pc = int(operands[2])
                taken = True
            else:
                correct_pc = pc + 1
                taken = False
        if op == 'bne':
            if rf[int(operands[0][1:])] != rf[int(operands[1][1:])]:
                correct_pc = int(operands[2])
                taken = True
            else:
                correct_pc = pc + 1
                taken = False
        if op == 'ble':
            if rf[int(operands[0][1:])] <= rf[int(operands[1][1:])]:
                correct_pc = int(operands[2])
                taken = True
            else:
                correct_pc = pc + 1
                taken = False
        if op == 'blt':
            if rf[int(operands[0][1:])] < rf[int(operands[1][1:])]:
                correct_pc = int(operands[2])
                taken = True
            else:
                correct_pc = pc + 1
                taken = False
        if op == 'j':
            correct_pc = int(operands[0])
            taken = True

        self.update_two_bit(pc, correct_pc, taken)
        if op != 'j':
            self.branches.append(executed)

        if next_pc == correct_pc:
            if op != 'j':
                self.correct += 1
            return (True, correct_pc)
        else:
            if op != 'j':
                self.incorrect += 1
            return (False, correct_pc)

    def update_two_bit(self, pc, correct_pc, taken):
        index = self.bht[pc][0] * 2 + self.bht[pc][1] + 2
        self.bht[pc][0] = self.bht[pc][1]
        if taken and self.bht[pc][index] < 3:
            self.btb[pc] = correct_pc
            self.bht[pc][index] += 1
        elif not taken and self.bht[pc][index] > 0:
            self.btb[pc] = correct_pc
            self.bht[pc][index] -= 1
        if taken:
            self.bht[pc][1] = 1
        else:
            self.bht[pc][1] = 0
