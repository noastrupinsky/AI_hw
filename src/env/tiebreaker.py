class TieBreaker:
    _instance = None  # Class-level variable to hold the single instance
     
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TieBreaker, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.max_g = 0
        self.c = 1
        
    def reset(self, curr_g):
        self.max_g = 0
        self.c = 1
        
    def updateMaxG(self, curr_g):
        self.max_g = max(self.max_g, curr_g)
        self.c = self.max_g + 1
    
    def tieBreaker(self, sucessor1, sucessor2):
        f1, g1 = sucessor1
        f2, g2 = sucessor2

        priorityA = (self.c * f1) - g1
        priorityB = (self.c * f2) - g2

        if priorityA > priorityB:
            return 1 ##succesor 1 is better
        else:    
            return 0
        