class ROB:

    class ROB_entry:
        def __init__(self):
            self.reg  = None
            self.val  = None
            self.done = None
    
    def __init__(self):
        self.entries = [ROB.ROB_entry()] * 2048
        self.commit  = 0
        self.issue   = 0


class RS:

    class RS_entry:
        def __init__(self, op, dest, tag1, tag2, val1, val2):
            self.op         = op
            self.dest       = dest
            self.tag1       = tag1
            self.tag2       = tag2
            self.val1       = val1
            self.val2       = val2
            self.dispatched = False
        
    def __init__(self):
        self.entries = [None] * 128

    def split(self, opcode, operands):
        if opcode == 'add':
            return (opcode, operands[0], operands[1], operands[2], None, None)

    def fill_next(self, op, dest, tag1, tag2, val1, val2):
        if None in self.entries:
            next_none = self.entries.index(None)
            self.entries[next_none] = RS.RS_entry(op, dest, tag1, tag2, val1, val2)


class Processor:
    def __init__(self):
        self.pc = 0

        self.iq = []
        self.rf = [0] * 32
        self.mem = []
        self.rob = ROB()
        self.rat = [None] * 128
        self.rs = RS()

        self.cycles = 0
        self.executed = 0
        self.array_labels = {}

    def cycle(self, assembly):
        instruction = self.fetch(assembly)
        opcode, operands = self.decode(instruction)
        self.issue(opcode, operands)
        # self.execute(opcode, operands, self.pc)
        # self.cycles += 3

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
    
    def issue(self, opcode, operands):
        op, dest, tag1, tag2, val1, val2 = self.rs.split(opcode, operands)
        # 1. Place next instruction from iq into the next available space in the rs.
        self.rs.fill_next(op, dest, tag1, tag2, val1, val2)
        # 2. Set the rob_entry.reg at the issue pointer to be the dest register of the instruction.
        #    Set the rob_entry.done to False.
        self.rob.entries[self.rob.issue].reg  = dest
        self.rob.entries[self.rob.issue].done = False
        # 3. Update the rat of the dest register to point to the rob_entry.
        self.rat[int(dest[1:])] = self.rob.entries[self.rob.issue]

    def dispatch(self):
        # 1. Check if operands are available and ready.
        # 2. Send the instruction to execute.
        #    The instruction carries a name (or tag) of the rob_entry used.
        # 3. Free the rs of the instruction.
        pass
    
    def write_back(self):
        # 1. Broadcast the name (or tag) and the value of the completed instruction
        #    back to the rs so that the rs can 'capture' the values.
        # 2. Place the broadcast value into the rob_entry used for that instruction.
        #    Set rob_entry.done to True
        pass
    
    def commit(self):
        # 1. Test if next instruction at commit pointer of rob is done.
        # 2. If it is done, commit:
        #        a. Write the rob_entry.val to the rob_entry.reg.
        #        b. If rob_entry is latest rename of rat for rob_entry.reg, 
        #               update rat to point to rob_entry.reg instead of rob_entry
        #           else:
        #               leave rat entry as is
        pass

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