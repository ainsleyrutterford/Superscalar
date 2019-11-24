class Pipe:
    def __init__(self, pc):
        self.pc = pc
        self.instruction = None
        self.opcode = None
        self.operand = None
        self.stage = 'Fetch'

class Processor:
    def __init__(self):
        self.pc = 0
        self.instruction_memory = []
        self.data_memory = []
        self.array_labels = {}
        self.registers = [0] * 32
        self.cycles = 0
        self.instructions_executed = 0
        self.pipeline = [None, None, None]

    def fill_next_pipe(self):
        next_none = self.pipeline.index(None)
        self.pipeline[next_none] = Pipe(self.pc)

    def flush_pipeline(self):
        self.pipeline = [None, None, None]
    
    def execute_pipes(self, assembly):
        fetches = 0
        branched = False
        for i, pipe in enumerate(self.pipeline):
            if pipe != None:
                if pipe.stage == 'Fetch':
                    pipe.instruction = self.fetch(assembly)
                    if not branched:
                        self.pc += 1
                    pipe.stage = 'Decode'
                elif pipe.stage == 'Decode':
                    (pipe.opcode, pipe.operand) = self.decode(pipe.instruction)
                    pipe.stage = 'Execute'
                elif pipe.stage == 'Execute':
                    branch = self.execute(pipe.opcode, pipe.operand, pipe.pc)
                    self.pipeline[i] = None
                    if branch:
                        branched = True
                        self.flush_pipeline()

    def cycle(self, assembly):
        self.fill_next_pipe()
        self.execute_pipes(assembly)
        self.cycles += 1

    def fetch(self, assembly):
        if (self.pc >= len(assembly.splitlines())):
            instruction = 'nop'
        else:
            instruction = assembly.splitlines()[self.pc]
        return instruction

    def decode(self, instruction):
        if (instruction[0] == '.'):
            label = instruction[1:instruction.find(':')]
            values = [int(x) for x in instruction.split(' ')[1:]]
            self.array_labels[label] = len(self.data_memory)
            self.data_memory += values
            opcode = 'nop'
            operands = []
        else:
            opcode = instruction[:instruction.find(' ')]
            operands = instruction.split(' ')[1:]
        return (opcode, operands)
    
    def execute(self, opcode, operands, pipe_pc):
        if   (opcode == 'addi'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] + int(operands[2])
        elif (opcode == 'add'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] + self.registers[int(operands[2][1:])]
        elif (opcode == 'sub'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])] - self.registers[int(operands[2][1:])]
        elif (opcode == 'beq'):
            if (self.registers[int(operands[0][1:])] == self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
                return True
        elif (opcode == 'bne'):
            if (self.registers[int(operands[0][1:])] != self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
                return True
        elif (opcode == 'ble'):
            if (self.registers[int(operands[0][1:])] <= self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
                return True
        elif (opcode == 'blt'):
            if (self.registers[int(operands[0][1:])] <  self.registers[int(operands[1][1:])]):
                self.pc = int(operands[2])
                return True
        elif (opcode == 'j'):
            self.pc = int(operands[0])
            return True
        elif (opcode == 'jr'):
            self.pc = self.registers[int(operands[0][1:])]
            return True
        elif (opcode == 'jal'):
            self.registers[29] = pipe_pc
            self.pc = int(operands[0])
            return True
        elif (opcode == 'li'):
            self.registers[int(operands[0][1:])] = int(operands[1])
        elif (opcode == 'lw'):
            array_op = operands[1]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                index = self.registers[int(index[1:])]
            else:
                index = int(index)
            data_index = self.array_labels[label] + index
            self.registers[int(operands[0][1:])] = self.data_memory[data_index]
        elif (opcode == 'sw'):
            array_op = operands[0]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                index = self.registers[int(index[1:])]
            else:
                index = int(index)
            data_index = self.array_labels[label] + index
            self.data_memory[data_index] = self.registers[int(operands[1][1:])]
        elif (opcode == 'move'):
            self.registers[int(operands[0][1:])] = self.registers[int(operands[1][1:])]
        self.instructions_executed += 1
        return False
    
    def is_running(self):
        if self.registers[31] == 0:
            return True
        else:
            return False