class Processor:
    def __init__(self):
        self.pc = 0
        self.instructions = []
        self.data = [0] * 100
        self.cycles = 0
        self.instructions_executed = 0
    
    def fetch(self, assembly):
        instruction = assembly.splitlines()[self.pc]
        self.pc = self.pc + 1
        return instruction
    
    def execute(self, instruction):
        opcode = instruction[:instruction.find(' ')]
        operands = instruction.split(' ')[1:]
        if   (opcode == 'addi'):
            self.data[int(operands[0][1:])] = self.data[int(operands[1][1:])] + int(operands[2])
        elif (opcode == 'add'):
            self.data[int(operands[0][1:])] = self.data[int(operands[1][1:])] + self.data[int(operands[2][1:])]
        elif (opcode == 'sub'):
            self.data[int(operands[0][1:])] = self.data[int(operands[1][1:])] - self.data[int(operands[2][1:])]
        elif (opcode == 'beq'):
            if (self.data[int(operands[0][1:])] == self.data[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'ble'):
            if (self.data[int(operands[0][1:])] <= self.data[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'j'):
            self.pc = int(operands[0])
        elif (opcode == 'li'):
            self.data[int(operands[0][1:])] = int(operands[1])