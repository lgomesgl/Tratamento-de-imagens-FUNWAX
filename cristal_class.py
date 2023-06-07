'''
    Create a class, the object is the crystal
'''
class CrystalsClassification:
    
    def __init__(self):
        self.is_crystal = False
        self.cnt_color = (0, 0, 255)
        
    def validate_the_crystal(self):
        self.is_crystal = True
        self.cnt_color = (0, 255, 0)
    
    def invalidate_the_crystal(self):
        self.is_crystal = False
        self.cnt_color = (0, 0, 255)
            
    def save(self):
        pass
    
    def return_(self):
        pass
    

        
        
    

    
    