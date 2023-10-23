from Island_classification_at_micro.island_crop import main_island
from Crystals.data import create_dataframes, separate_the_data_by_column, save_the_data, data_n_of_crystals, data_each_image
from Crystals.classification_crystals import get_files, get_properties, images_to_verify, get_image, crop_the_image, filter, classification, images_to_crop
from Statistic.hierarchy_erro import hierarchy_erro
from Processing.dynamic import dist_image
from Processing.pos import graphics, hierarchy

# Variables
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
# FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images_test1'
NAME_CSV_DATA = 'Results_crystals.csv'
NAME_CSV_DATA_CRYSTALS = 'Results_number_of_crystals.csv'

def main(island, scale_crop):
    # Data
    # data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'cx', 'cy', 'major', 'minor', 'angle', 'AR'])
    data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time','Island','AR'])
    data_crystals = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals','Parent(%)','Child(%)','No Parent/Child(%)'])
    
    # List
    n_of_crystals_ = [0]
    num_image = []

    # Code    
    if island:   
        main_island(FOLDER_PATH) # crop the island from micro type images
            
    print('Start to classify the crystals')
    files = get_files(FOLDER_PATH) 
    for file in files:
        properties = get_properties(file)
        
        if images_to_verify(properties, island):
            image = get_image(FOLDER_PATH, file)
            
            if properties[1] in images_to_crop(island):
                image = crop_the_image(image, scale_crop)
            
            contours, hierarchy = filter(image, properties)
            data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties)

            n_of_crystals_.append(n_of_crystals)
            data_crystals = data_n_of_crystals(data_crystals, properties, n_of_crystals_, perct_parent, perct_child, perct_else)

            # df = data_each_image(data,num_image,n_of_crystals)
            # dist_image(df)
            
            print('%s...Ok' % file)
        
    # update the data
    save_the_data(data, NAME_CSV_DATA) 
    save_the_data(data_crystals, NAME_CSV_DATA_CRYSTALS)

    # dataframes = separate_the_data_by_column(data, 'kernel')

    graphics(data, data_crystals)
    # hierarchy(data_crystals)
    
    print(hierarchy_erro())
    
    return data, data_crystals

data, data_crystals = main(island=True, scale_crop=0.5)