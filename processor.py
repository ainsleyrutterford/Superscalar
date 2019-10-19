class Processor:
    def __init__(self):
        self.pc = 0
        self.instruction_memory = []
        self.data_memory = []
        self.array_labels = {}
        self.registers = [0] * 20
        self.cycles = 0
        self.instructions_executed = 0
    
    def fetch(self, assembly):
        instruction = assembly.splitlines()[self.pc]
        self.pc = self.pc + 1
        return instruction
    
    def execute(self, instruction):
        if (instruction[0] == '.'):
            label = instruction[1:instruction.find(' ')]
            values = [int(x) for x in instruction.split(' ')[1:]]
            self.array_labels[label] = len(data_memory)
            self.data_memory += values
            return
        opcode = instruction[:instruction.find(' ')]
        operands = instruction.split(' ')[1:]
        if   (opcode == 'addi'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] + int(operands[2])
            return
        elif (opcode == 'add'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] + self.registers[int(operands[2][1:])]
            return
        elif (opcode == 'sub'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] - self.registers[int(operands[2][1:])]
            return
        elif (opcode == 'beq'):
            if (self.registers[int(operands[0][1:])] == self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
            return
        elif (opcode == 'ble'):
            if (self.registers[int(operands[0][1:])] <= self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
            return
        elif (opcode == 'blt'):
            if (self.registers[int(operands[0][1:])] <  self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
            return
        elif (opcode == 'j'):
            self.pc = int(operands[0])
            return
        elif (opcode == 'li'):
            self.registers[int(operands[0][1:])] = int(operands[1])
            return
        elif (opcode == 'lw'):
            array_op = operands[1]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                index = self.registers[int(index[1:])]
            else:
                index = int(index)
            data_index = array_labels[label] + index
            self.registers[int(operands[0][1:])] = self.data_memory[data_index]
            return
        elif (opcode == 'sw'):
            
        elif (opcode == 'move'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])]
            return