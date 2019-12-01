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