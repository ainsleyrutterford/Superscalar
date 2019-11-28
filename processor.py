class ROB:

    class ROB_entry:
        def __init__(self):
            self.reg  = None
            self.val  = None
            self.done = None
    
    def __init__(self):
        self.entries = [ROB.ROB_entry()] * 128
        self.commit  = 0
        self.issue   = 0


class RS:

    class RS_entry:
        def __init__(self):
            self.busy       = False
            self.op         = None
            self.val1       = None
            self.val2       = None
            self.wait1      = None
            self.wait2      = None
            self.dispatched = False
        
    def __init__(self):
        self.entries = [RS.RS_entry()] * 128


class Processor:
    def __init__(self):
        self.pc = 0
        self.iq = []
        self.mem = []
        self.array_labels = {}
        self.rf = [0] * 32
        self.cycles = 0
        self.executed = 0
        self.rob = ROB()
        self.rat = [0] * 128
        self.rs = RS()

    def cycle(self, assembly):
        instruction = self.fetch(assembly)
        opcode, operands = self.decode(instruction)
        self.execute(opcode, operands, self.pc)
        self.cycles += 3

    def fetch(self, assembly):
        if (self.pc >= len(assembly.splitlines())):
            instruction = 'nop'
        else:
            instruction = assembly.splitlines()[self.pc]
        self.pc += 1
        return instruction

    def decode(self, instruction):
        if (instruction[0] == '.'):
            label = instruction[1:instruction.find(':')]
            values = [int(x) for x in instruction.split(' ')[1:]]
            self.array_labels[label] = len(self.mem)
            self.mem += values
            opcode = 'nop'
            operands = []
        else:
            opcode = instruction[:instruction.find(' ')]
            operands = instruction.split(' ')[1:]
        return (opcode, operands)
    
    def execute(self, opcode, operands, current_pc):
        if   (opcode == 'addi'):
            self.rf[int(operands[0][1:])] = self.rf[int(operands[1][1:])] + int(operands[2])
        elif (opcode == 'add'):
            self.rf[int(operands[0][1:])] = self.rf[int(operands[1][1:])] + self.rf[int(operands[2][1:])]
        elif (opcode == 'sub'):
            self.rf[int(operands[0][1:])] = self.rf[int(operands[1][1:])] - self.rf[int(operands[2][1:])]
        elif (opcode == 'beq'):
            if (self.rf[int(operands[0][1:])] == self.rf[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'bne'):
            if (self.rf[int(operands[0][1:])] != self.rf[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'ble'):
            if (self.rf[int(operands[0][1:])] <= self.rf[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'blt'):
            if (self.rf[int(operands[0][1:])] <  self.rf[int(operands[1][1:])]):
                self.pc = int(operands[2])
        elif (opcode == 'j'):
            self.pc = int(operands[0])
        elif (opcode == 'jr'):
            self.pc = self.rf[int(operands[0][1:])]
        elif (opcode == 'jal'):
            self.rf[29] = current_pc
            self.pc = int(operands[0])
        elif (opcode == 'li'):
            self.rf[int(operands[0][1:])] = int(operands[1])
        elif (opcode == 'lw'):
            array_op = operands[1]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                index = self.rf[int(index[1:])]
            else:
                index = int(index)
            data_index = self.array_labels[label] + index
            self.rf[int(operands[0][1:])] = self.mem[data_index]
        elif (opcode == 'sw'):
            array_op = operands[0]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                index = self.rf[int(index[1:])]
            else:
                index = int(index)
            data_index = self.array_labels[label] + index
            self.mem[data_index] = self.rf[int(operands[1][1:])]
        elif (opcode == 'move'):
            self.rf[int(operands[0][1:])] = self.rf[int(operands[1][1:])]
        self.executed += 1
    
    def is_running(self):
        if self.rf[31] == 0:
            return True
        else:
            return False