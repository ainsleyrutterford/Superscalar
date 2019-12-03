class Predictor:

    predict = lambda: None

    def __init__(self, method):
        if method == 'not_taken':
            self.predict = self.not_taken
        elif method == 'two_bit':
            self.predict = self.two_bit
    
    def not_taken(self, pc):
        return pc + 1

    def two_bit(self):
        pass
    
    def check(self, rf, op, operands, pc, next_pc):
        correct_pc = next_pc
        if op == 'blt':
            if (rf[int(operands[0][1:])] <  rf[int(operands[1][1:])]):
                correct_pc = int(operands[2])
        if next_pc == correct_pc:
            return (True, correct_pc)
        else:
            return (False, correct_pc)