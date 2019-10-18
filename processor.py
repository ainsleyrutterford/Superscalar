class Processor:
    def __init__(self):
        self.pc    = 0
        self.instructions = []
        self.data = []
    
    def fetch(self, assembly):
        instruction = assembly[self.pc]
        self.pc = self.pc + 1
        return instruction
    
    def execute(self, instruction):
        opcode = instruction[:instruction.find(' ')]
        operands = instruction.split(' ')[1:]
        if   (opcode == 'addi'):
            data[operands[0]] = data[operands[1]] + operands[2]
        elif (opcode == 'sub'):
            data[operands[0]] = data[operands[1]] - data[operands[2]]
        elif (opcode == 'beq'):
            if (data[operands[0]] == data[operands[1]]):
                pc = operands[2]
        elif (opcode == 'ble'):
            if (data[operands[0]] <= data[operands[1]]):
                pc = operands[2]
        elif (opcode == 'j'):
            pc = operands[0]