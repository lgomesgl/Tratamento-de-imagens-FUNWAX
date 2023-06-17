from cristal_class import CrystalsClassification

def accept():
    crystal = CrystalsClassification()
    while True:
        check = input()
        if check == 1:
            crystal.validate_the_crystal()
            
        elif check == 2:
            crystal.invalidate_the_crystal()
            
        print(crystal.is_crystal)
        
        return check
    
