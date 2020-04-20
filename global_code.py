class constants:
    DATA_PATH = 'Data/' 
    
class functions:
    def globalUtilTestFunc():
        #do something on a global scale
        return 1+1
    
  
class TimerInterval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
class InclusiveTimeInterval:
    def __init__(self, start_inkl, end_inkl):
        super.__init__(start_inkl, end_inkl)
        self.start_included = True
        self.end_included = True
    