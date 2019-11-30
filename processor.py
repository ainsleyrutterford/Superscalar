import opcodes

class ROB:

    class ROB_entry:
        def __init__(self):
            self.reg  = None
            self.val  = None
            self.done = None
    
    def __init__(self):
        self.entries = [ROB.ROB_entry() for i in range(2048)]
        self.commit  = 0
        self.issue   = 0


class RS:

    class RS_entry:
        def __init__(self, op, dest_tag, tag1, tag2, val1, val2):
            self.op         = op
            self.dest_tag   = dest_tag
            self.tag1       = tag1
            self.tag2       = tag2
            self.val1       = val1
            self.val2       = val2
            self.dispatched = False
        
    def __init__(self):
        self.entries = [None] * 128

    def split(self, op_tuple):
        opcode = op_tuple[0]
        operands = op_tuple[1]
        if opcode in opcodes.arithmetic_ops:
            return (opcode, operands[0], operands[1], operands[2], None, None)

    def fill_next(self, op, dest_tag, tag1, tag2, val1, val2):
        if None in self.entries:
            next_none = self.entries.index(None)
            self.entries[next_none] = RS.RS_entry(op, dest_tag, tag1, tag2, val1, val2)
    
    def find_next_ready(self):
        for i, entry in enumerate(self.entries):
            if entry != None:
                if entry.val1 != None and entry.val2 != None and entry.dispatched == False:
                    return i

    def capture(self, tag, val):
        for entry in self.entries:
            if entry != None:
                if entry.tag1 == tag:
                    entry.val1 = val
                    entry.tag1 = None
                if entry.tag2 == tag:
                    entry.val2 = val
                    entry.tag2 = None

class Processor:
    def __init__(self):
        self.pc = 0

        self.iq = []
        self.opq = []
        # self.rf = [0] * 32
        self.rf = [12, 4, 7, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.mem = []
        self.rob = ROB()
        self.rat = [None] * 128
        self.rs = RS()
        self.eq = []
        self.wbq = []

        self.cycles = 0
        self.executed = 0
        self.array_labels = {}

    def cycle(self, assembly):
        self.commit()
        self.write_back()
        if len(self.eq) > 0:
            self.execute()
        self.dispatch()
        if len(self.opq) > 0:
            self.issue(self.opq.pop(0))
        if len(self.iq) > 0:
            self.opq.append(self.decode(self.iq.pop(0)))
        if self.pc < len(assembly.splitlines()):
            self.iq.append(self.fetch(assembly))
        self.cycles += 1
        print(f'cycle: {self.cycles}')
        print(f'instruction queue: {self.iq}')
        print(f'op queue: {self.opq}')
        print(f'register file: {self.rf}')
        print(f'rob: { [f"{e.reg}, {e.val}, {e.done}" for e in self.rob.entries[:6]] }')
        print(f'rat: {self.rat[:6]}')
        print(f'res station: { [f"{rs.op}, {rs.dest_tag}, {rs.tag1}, {rs.tag2}, {rs.val1}, {rs.val2}" for rs in filter(None, self.rs.entries[:6])] }')
        print(f'writeback queue: {self.wbq}')

    def fetch(self, assembly):
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
            if instruction == 'nop':
                opcode = 'nop'
                operands = []
            else:
                opcode = instruction[:instruction.find(' ')]
                operands = instruction.split(' ')[1:]
        return (opcode, operands)
    
    def issue(self, op_tuple):
        op, dest, tag1, tag2, val1, val2 = self.rs.split(op_tuple)
        # 1. Place next instruction from iq into the next available space in the rs.
        if self.rat[int(tag1[1:])] == None:
            val1 = self.rf[int(tag1[1:])]
            tag1 = None
        else:
            tag1 = self.rat[int(tag1[1:])]
        if self.rat[int(tag2[1:])] == None:
            val2 = self.rf[int(tag2[1:])]
            tag2 = None
        else:
            tag2 = self.rat[int(tag2[1:])]
        self.rs.fill_next(op, self.rob.issue, tag1, tag2, val1, val2)
        # 2. Set the rob_entry.reg at the issue pointer to be the dest register of the instruction.
        #    Set the rob_entry.done to False.
        self.rob.entries[self.rob.issue].reg  = int(dest[1:])
        self.rob.entries[self.rob.issue].done = False
        # 3. Update the rat of the dest register to point to the rob_entry.
        self.rat[int(dest[1:])] = self.rob.issue
        # Increment the rob issue pointer.
        self.rob.issue += 1

    def dispatch(self):
        # 1. Check if operands are available and ready.
        ready_index = self.rs.find_next_ready()
        if ready_index != None:
            op = self.rs.entries[ready_index].op
            if self.execute_available(op):
                # 2. Send the instruction to execute.
                #    The instruction carries a name (or tag) of the rob_entry used.
                self.eq.append( self.rs.entries[ready_index] )
                # 3. Free the rs of the instruction.
                self.rs.entries[ready_index] = None
    
    def write_back(self):
        self.decrement_wbq_cycles()
        if len(self.wbq) > 0:
            # Only write back if it has been enough cycles
            if self.wbq[0][2] == 0:
                # 1. Broadcast the name (or tag) and the value of the completed instruction
                #    back to the rs so that the rs can 'capture' the values.
                tag, val, cycles, op = self.wbq.pop(0)
                self.rs.capture(tag, val)
                # 2. Place the broadcast value into the rob_entry used for that instruction.
                #    Set rob_entry.done to True
                self.rob.entries[tag].val = val
                self.rob.entries[tag].done = True
    
    def commit(self):
        # 1. Test if next instruction at commit pointer of rob is done.
        # 2. If it is done, commit:
        #        a. Write the rob_entry.val to the rob_entry.reg.
        #        b. If rob_entry is latest rename of rat for rob_entry.reg, 
        #               update rat to point to rob_entry.reg instead of rob_entry
        #           else:
        #               leave rat entry as is
        rob_entry = self.rob.entries[self.rob.commit]
        if rob_entry.done == True:
            self.rf[rob_entry.reg] = rob_entry.val
            reg = self.rob.entries[self.rob.commit].reg
            if self.rat[reg] == self.rob.commit:
                self.rat[reg] = None
            self.rob.entries[self.rob.commit] = ROB.ROB_entry()
            self.rob.commit += 1


    def execute(self):
        rs_entry = self.eq.pop(0)
        if rs_entry.op == 'add':
            # Third entry is how many cycles it will take to execute
            self.wbq.append( [rs_entry.dest_tag, rs_entry.val1 + rs_entry.val2, 2, rs_entry.op] )
        if rs_entry.op == 'sub':
            self.wbq.append( [rs_entry.dest_tag, rs_entry.val1 - rs_entry.val2, 2, rs_entry.op] )


    def execute_old(self, opcode, operands, current_pc):
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
    
    def execute_available(self, op):
        in_use = 0
        if op in opcodes.arithmetic_ops:
            in_use = sum(1 for wb in self.wbq if wb[3] in opcodes.arithmetic_ops)
        if in_use < 2:
            return True
        else:
            return False

    def decrement_wbq_cycles(self):
        if len(self.wbq) > 0:
            for wb in self.wbq:
                wb[2] -= 1

    def is_running(self):
        if self.rf[31] == 0:
            return True
        else:
            return False