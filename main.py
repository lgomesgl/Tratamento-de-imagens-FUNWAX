from Island_classification_at_micro.island_crop import main_island
from Classification.data import create_dataframes, separate_the_data_by_column, save_the_data, exclude_the_data, data_n_of_crystals
from Classification.classification_crystals import get_properties, get_image, crop_the_image, filter, classification, images_to_verify, get_files
from Classification.pos_processing import graphics

# Variables
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
NAME_CSV_FILE = 'Results_crystals.csv'

data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'AR'])
data_crystals = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])
n_of_crystals_ = [0]

# Code
# exclude_the_data(FOLDER_PATH, NAME_CSV_FILE) # exclude the data to update the csv file
        
# print('Start to crop the island at micro images')   
# main_island(FOLDER_PATH) # crop the island  
        
print('Start to classify the crystals')
files = get_files(FOLDER_PATH)# list with all files in folder
for i, file in enumerate(files):
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
    
save_the_data(data, NAME_CSV_FILE) # update the data

# dataframes = separate_the_data_by_column(data, 'kernel')

graphics(data, data_crystals)

