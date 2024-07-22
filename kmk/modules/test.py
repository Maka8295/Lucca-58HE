from kmk.modules import Module
from keypad import Event as KeyEvent

class test(Module):
    
    def __init__(self):
        print("init")
    def before_matrix_scan(self, keyboard):
        print("ho")
        return 
    
    