from logger import IOLogger 
logger = IOLogger(10) 

#constants
class constants:
    DATA_PATH = 'Data/' 

    
#functions
def getLogger():
    return logger    
  

#public classes
class TimerInterval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
class InclusiveTimeInterval:
    def __init__(self, start_inkl, end_inkl):
        super.__init__(start_inkl, end_inkl)
        self.start_included = True
        self.end_included = True
    