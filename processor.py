import opcodes
import predictor

class ROB:

    class ROB_entry:
        def __init__(self):
            self.reg     = None
            self.val     = None
            self.done    = None
            self.load    = False
            self.branch  = False
            self.allowed = None
    
    def __init__(self):
        self.entries = [ROB.ROB_entry() for i in range(2048)]
        self.commit  = 0
        self.issue   = 0
    
    def fill_branch_info(self, op_tuple):
        self.entries[self.issue].op = op_tuple[0]
        self.entries[self.issue].operands = op_tuple[1]
        self.entries[self.issue].current_pc = op_tuple[2]
        self.entries[self.issue].next_pc = op_tuple[3]
        self.entries[self.issue].branch = True

    def decrement_allowed_counters(self):
        for entry in self.entries:
            if entry.done and entry.allowed != None:
                entry.allowed -= 1

class LSQ:

    class LSQ_entry:
        def __init__(self):
            self.op        = None
            self.dest_tag  = None
            self.base_addr = None
            self.addr      = None
            self.val       = None
            self.reg       = None
            self.done      = None
            self.wait_tag  = None
            self.allowed   = 1
    
    def __init__(self):
        self.entries = [LSQ.LSQ_entry() for i in range(2048)]
        self.commit  = 0
        self.issue   = 0
        self.array_labels = {}
    
    def find_dest_and_addr(self, op_tuple, dest_tag, rat, rf):
        op = op_tuple[0]
        operands = op_tuple[1]
        if op == 'lw':
            array_op = operands[1]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                if rat[int(index[1:])] == None:
                    wait_tag = None
                    index = rf[int(index[1:])]
                else:
                    wait_tag = rat[int(index[1:])]
                    index = None
            else:
                wait_tag = None
                index = int(index)
            base_address = self.array_labels[label]
            dest = operands[0]
        elif op == 'sw':
            array_op = operands[0]
            label = array_op[:array_op.find('(')]
            index = array_op[array_op.find('(')+1:array_op.find(')')]
            if (index.startswith('$')):
                if rat[int(index[1:])] == None:
                    wait_tag = None
                    index = rf[int(index[1:])]
                else:
                    wait_tag = rat[int(index[1:])]
                    index = None
            else:
                wait_tag = None
                index = int(index)
            base_address = self.array_labels[label]
            self.entries[self.issue].reg = int(operands[1][1:])
            dest = '$32'
        self.entries[self.issue].op        = op
        self.entries[self.issue].dest_tag  = dest_tag
        self.entries[self.issue].base_addr = base_address
        if index != None:
            self.entries[self.issue].addr  = base_address + index
        self.entries[self.issue].done      = False
        self.entries[self.issue].wait_tag  = wait_tag
        return dest
    
    def find_next_ready(self):
        for i, entry in enumerate(self.entries):
            if entry.op != None and not entry.done and entry.wait_tag == None and entry.allowed < 0:
                entry.done = True
                return i

    def can_forward(self, address):
        latest = None
        for i, entry in enumerate(self.entries):
            if entry.addr == address and entry.op == 'sw':
                latest = i
        return latest
    
    def capture(self, wait_tag, val):
        for entry in self.entries:
            if entry != None:
                if entry.wait_tag == wait_tag:
                    entry.addr = entry.base_addr + val
                    entry.wait_tag = None

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
            self.allowed    = 1
        
    def __init__(self):
        self.entries = [None] * 128

    def split(self, op_tuple):
        opcode = op_tuple[0]
        operands = op_tuple[1]
        if opcode in (opcodes.arithmetic + opcodes.advanced):
            return (opcode, operands[0], operands[1], operands[2], None, None)
        if opcode in (opcodes.immediate):
            return (opcode, operands[0], operands[1], None, None, int(operands[2]))

    def fill_next(self, op, dest_tag, tag1, tag2, val1, val2):
        if None in self.entries:
            next_none = self.entries.index(None)
            self.entries[next_none] = RS.RS_entry(op, dest_tag, tag1, tag2, val1, val2)
    
    def fill_next_branch(self, op_tuple, dest_tag):
        if None in self.entries:
            next_none = self.entries.index(None)
            self.entries[next_none] = RS.RS_entry(op_tuple[0], dest_tag, None, None, 0, 0)

    def find_next_ready(self):
        ready = None
        index = float('inf')
        for i, entry in enumerate(self.entries):
            if entry != None:
                if entry.val1 != None and entry.val2 != None and entry.dispatched == False and entry.allowed < 0:
                    if entry.dest_tag < index: # Always return oldest entry
                        ready = i
                        index = entry.dest_tag
        return ready

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
        self.rf = [0] * 33 # (32 and an extra as a dummy for sw ROB entries)
        self.mem = []
        self.rob = ROB()
        self.lsq = LSQ()
        self.rat = [None] * 128
        self.rs = RS()
        self.eq = []
        self.wbq = []

        self.new_iq  = []
        self.new_opq = []
        self.new_eq  = []

        self.predictor = predictor.Predictor('two_bit')
        self.super = 4
        self.cycles = 0
        self.executed = 0

    def cycle(self, assembly):
        self.new_iq  = []
        self.new_opq = []
        self.new_eq  = []

        # Fetch
        for i in range(self.super):
            if self.pc < len(assembly.splitlines()):
                self.new_iq.append(self.fetch(assembly))

        # Decode
        for i in range(self.super):
            if len(self.iq) > 0:
                self.new_opq.append(self.decode(self.iq.pop(0)))

        # Issue
        for i in range(self.super):
            if len(self.opq) > 0:
                self.issue(self.opq.pop(0))

        # Dispatch
        self.decrement_rs_and_lsq_counters()
        for i in range(self.super):
            self.new_eq += self.dispatch()

        # Execute
        for i in range(self.super):
            if len(self.eq) > 0:
                self.execute(self.eq.pop(0))

        # Writeback
        self.decrement_wbq_cycles()
        for i in range(self.super):
            self.write_back()

        self.iq  += self.new_iq
        self.opq += self.new_opq
        self.eq  += self.new_eq
        
        self.cycles += 1

        self.print_stats()

    def fetch(self, assembly):
        instruction = assembly.splitlines()[self.pc]
        original_pc = self.pc
        next_pc = self.predictor.predict(self.pc, instruction)
        self.pc = next_pc
        return instruction, original_pc, next_pc

    def decode(self, tuple):
        instruction = tuple[0]
        original_pc = tuple[1]
        next_pc     = tuple[2]
        if (instruction[0] == '.'):
            label = instruction[1:instruction.find(':')]
            values = [int(x) for x in instruction.split(' ')[1:]]
            self.lsq.array_labels[label] = len(self.mem)
            self.mem += values
            opcode = 'add'
            operands = ['$32','$32','$32']
        else:
            opcode = instruction[:instruction.find(' ')]
            operands = instruction.split(' ')[1:]
        return (opcode, operands, original_pc, next_pc)
    
    def issue(self, op_tuple):
        if op_tuple[0] in (opcodes.arithmetic + opcodes.advanced + opcodes.immediate):
            op, dest, tag1, tag2, val1, val2 = self.rs.split(op_tuple)
            # 1. Place next instruction from iq into the next available space in the rs.
            if self.rat[int(tag1[1:])] == None:
                val1 = self.rf[int(tag1[1:])]
                tag1 = None
            else:
                tag1 = self.rat[int(tag1[1:])]
            if op not in opcodes.immediate:
                if self.rat[int(tag2[1:])] == None:
                    val2 = self.rf[int(tag2[1:])]
                    tag2 = None
                else:
                    tag2 = self.rat[int(tag2[1:])]
            if op in opcodes.immediate:
                op = op[:-1]
            self.rs.fill_next(op, self.rob.issue, tag1, tag2, val1, val2)
        elif op_tuple[0] in opcodes.memory:
            dest = self.lsq.find_dest_and_addr(op_tuple, self.rob.issue, self.rat, self.rf)
            self.lsq.issue += 1
            self.rob.entries[self.rob.issue].load = True
        elif op_tuple[0] in opcodes.branch:
            self.rs.fill_next_branch(op_tuple, self.rob.issue)
            self.rob.fill_branch_info(op_tuple)
            dest = '$32'
        # 2. Set the rob_entry.reg at the issue pointer to be the dest register of the instruction.
        #    Set the rob_entry.done to False.
        self.rob.entries[self.rob.issue].reg  = int(dest[1:])
        self.rob.entries[self.rob.issue].done = False
        # 3. Update the rat of the dest register to point to the rob_entry.
        self.rat[int(dest[1:])] = self.rob.issue
        # Increment the rob issue pointer.
        self.rob.issue += 1

    def dispatch(self):
        ready_entries = []
        # 1. Check if operands are available and ready.
        ready_index = self.rs.find_next_ready()
        if ready_index != None:
            op = self.rs.entries[ready_index].op
            # if self.execute_available(op):
            # 2. Send the instruction to execute.
            #    The instruction carries a name (or tag) of the rob_entry used.
            ready_entries.append(self.rs.entries[ready_index])
            # 3. Free the rs of the instruction.
            self.rs.entries[ready_index] = None
        lsq_ready = self.lsq.find_next_ready()
        if lsq_ready != None:
            op = self.lsq.entries[lsq_ready].op
            # if self.execute_available(op):
            # 2. Send the instruction to execute.
            #    The instruction carries a name (or tag) of the rob_entry used.
            ready_entries.append(self.lsq.entries[lsq_ready])
            # 3. Free the rs of the instruction.
            # self.lsq.entries[lsq_ready] = LSQ.LSQ_entry()
        return ready_entries

    def execute(self, entry):
        # Could be a reservation station entry or a load store queue entry
        allowed = 1

        if isinstance(entry, RS.RS_entry):
            if entry.op == 'add':
                # Third entry is how many cycles it will take to execute
                self.wbq.append( [entry.dest_tag, entry.val1 + entry.val2, 1, entry.op, allowed] )
            if entry.op == 'sub':
                self.wbq.append( [entry.dest_tag, entry.val1 - entry.val2, 1, entry.op, allowed] )
            if entry.op == 'mul':
                self.wbq.append( [entry.dest_tag, entry.val1 * entry.val2, 2, entry.op, allowed] )
            
            if entry.op in opcodes.branch:
                self.wbq.append( [entry.dest_tag, 0, 1, entry.op, allowed] )

        elif isinstance(entry, LSQ.LSQ_entry):
            if entry.op == 'lw':
                # Maybe do forwarding here?
                # forwarding = self.lsq.can_forward(entry.addr)
                # if forwarding != None:
                #     self.wbq.append( [entry.dest_tag, self.lsq.entries[forwarding].val, 1, 'lw'] )
                # else:
                if (entry.addr >= len(self.mem)):
                    # Branch misprediction here so just dont execute, it should be sorted at commit
                    self.wbq.append( [entry.dest_tag, -1, 2, 'lw', allowed] )
                else:
                    self.wbq.append( [entry.dest_tag, self.mem[entry.addr], 2, 'lw', allowed] )
            if entry.op == 'sw':
                self.wbq.append( [entry.dest_tag, 0, 1, 'sw', allowed] )

    def write_back(self):
        if len(self.wbq) > 0:
            # Only write back if it has been enough cycles
            if self.wbq[0][2] <= 0 and self.wbq[0][4] < 0:
                # 1. Broadcast the name (or tag) and the value of the completed instruction
                #    back to the rs so that the rs can 'capture' the values.
                tag, val, cycles, op, allowed = self.wbq.pop(0)
                self.rs.capture(tag, val)
                self.lsq.capture(tag, val)
                # 2. Place the broadcast value into the rob_entry used for that instruction.
                #    Set rob_entry.done to True
                self.rob.entries[tag].val = val
                self.rob.entries[tag].done = True
                if op == 'lw':
                    self.lsq.entries[tag].val = val
        # Commit
        # 1. Test if next instruction at commit pointer of rob is done.
        # 2. If it is done, commit:
        #        a. Write the rob_entry.val to the rob_entry.reg.
        #        b. If rob_entry is latest rename of rat for rob_entry.reg, 
        #               update rat to point to rob_entry.reg instead of rob_entry
        #           else:
        #               leave rat entry as is
        rob_entry = self.rob.entries[self.rob.commit]
        load = rob_entry.load
        branch = rob_entry.branch
        if rob_entry.done == True:
            self.rf[rob_entry.reg] = rob_entry.val
            if self.rat[rob_entry.reg] == self.rob.commit:
                self.rat[rob_entry.reg] = None
            self.rob.entries[self.rob.commit] = ROB.ROB_entry()
            self.rob.commit += 1
            if load:
                lsq_entry = self.lsq.entries[self.lsq.commit]
                if lsq_entry.op == 'sw':
                    self.mem[lsq_entry.addr] = self.rf[lsq_entry.reg]
                self.lsq.entries[self.lsq.commit] = LSQ.LSQ_entry()
                self.lsq.commit += 1
            if branch:
                correct, pc = self.predictor.check(self.rf, rob_entry.op, 
                rob_entry.operands, rob_entry.current_pc, rob_entry.next_pc)
                if not correct:
                    self.iq = []
                    self.opq = []
                    self.rob = ROB()
                    array_labels = self.lsq.array_labels
                    self.lsq = LSQ()
                    self.lsq.array_labels = array_labels
                    self.rat = [None] * 128
                    self.rs = RS()
                    self.eq = []
                    self.wbq = []
                    self.pc = pc
                    self.new_iq  = []
                    self.new_opq = []
                    self.new_eq  = []
            self.executed += 1

    def execute_available(self, op):
        in_use = 0
        if op in opcodes.arithmetic:
            in_use = sum(1 for wb in self.wbq if wb[3] in opcodes.arithmetic)
            return in_use < 2
        if op in opcodes.advanced:
            in_use = sum(1 for wb in self.wbq if wb[3] in opcodes.advanced)
            return in_use < 1
        if op in opcodes.memory:
            in_use = sum(1 for wb in self.wbq if wb[3] in opcodes.memory)
            return in_use < 1
        if op in opcodes.branch:
            in_use = sum(1 for wb in self.wbq if wb[3] in opcodes.branch)
            return in_use < 1

    def decrement_wbq_cycles(self):
        if len(self.wbq) > 0:
            for wb in self.wbq:
                wb[2] -= 1
                wb[4] -= 1
    
    def decrement_rs_and_lsq_counters(self):
        for entry in self.lsq.entries:
            if entry.op != None:
                entry.allowed -= 1
        for entry in self.rs.entries:
            if entry != None:
                entry.allowed -= 1

    def is_running(self):
        if self.rf[31] == 0:
            return True
        else:
            return False
    
    def print_stats(self):
        print(f'cycle: {self.cycles}')
        print(f'executed: {self.executed}')
        print(f'instruction queue: {self.iq}')
        print(f'op queue: {self.opq}')
        print(f'register file: {self.rf}')
        print(f'rob: { [f"{e.reg}, {e.val}, {e.done}" for e in self.rob.entries[:10]] }')
        print(f'lsq: { [f"{e.op}, {e.dest_tag}, {e.addr}, {e.val}, {e.done}" for e in self.lsq.entries[:10]] }')
        print(f'rat: {self.rat[:20]}')
        print(f'res station: { [f"{rs.op}, {rs.dest_tag}, {rs.tag1}, {rs.tag2}, {rs.val1}, {rs.val2}" for rs in filter(None, self.rs.entries[:6])] }')
        # print(f'exec queue: { [f"{rs.op}, {rs.dest_tag}, {rs.tag1}, {rs.tag2}, {rs.val1}, {rs.val2}" for rs in filter(None, self.eq[:6])] }')
        print(f'writeback queue: {self.wbq}')
        print(f'memory: {self.mem}')