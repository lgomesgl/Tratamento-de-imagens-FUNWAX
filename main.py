from Island_classification_at_micro.island_crop import main_island
from Classification.data import create_dataframes, separate_the_data_by_column, save_the_data, data_n_of_crystals
from Classification.classification_crystals import get_properties, get_image, crop_the_image, filter, classification, images_to_verify, get_files
from Classification.pos_processing import graphics

# Variables
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
NAME_CSV_DATA = 'Results_crystals.csv'
NAME_CSV_DATA_CRYSTALS = 'Results_number_of_crystals.csv'

data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'AR'])
data_crystals = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])
n_of_crystals_ = [0]

# Code        
print('Start to crop the island at micro images')   
main_island(FOLDER_PATH) # crop the island  
        
print('Start to classify the crystals')
files = get_files(FOLDER_PATH)# list with all files in folder
for file in files:
    properties = get_properties(file)
    
    if images_to_verify(properties):
        image = get_image(FOLDER_PATH, file)
        
        if properties[1] == 'Macro':
            image = crop_the_image(image, 0.4)
        
        contours = filter(image, properties)
        data, n_of_crystals = classification(image, data, contours, properties)

        n_of_crystals_.append(n_of_crystals)
        data_crystals = data_n_of_crystals(data_crystals, properties, n_of_crystals_)
    
        print('%s...Ok' % file)
    
save_the_data(data, NAME_CSV_DATA) # update the data
save_the_data(data_crystals, NAME_CSV_DATA_CRYSTALS)

# dataframes = separate_the_data_by_column(data, 'kernel')

graphics(data, data_crystals)

