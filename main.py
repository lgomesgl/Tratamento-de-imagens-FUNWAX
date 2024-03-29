from Islands_at_micro.island_crop import main_island, delete_islands
from Crystals.data import create_dataframes, separate_the_data_by_column, save_the_data, data_n_of_crystals, data_each_image
from Crystals.classification_crystals import get_files, get_properties, images_to_verify, get_image, crop_the_image, filter, filter_nucleated_crystals, filter_non_nucleated_crystals, classification, images_to_crop, status_color_image
from Statistic.hierarchy_erro import hierarchy_erro
from Data_visualization.dynamic import dist_image
from Data_visualization.pos import graphics

# Variables
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\ImageNew'
# FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images_test1'
NAME_CSV_DATA = 'Results_crystals.csv'
NAME_CSV_DATA_CRYSTALS = 'Results_number_of_crystals.csv'

def main(island, scale_crop):
    # Data
    data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time','Island','AR','Status'])
    data_crystals = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals','Parent(%)','Child(%)','No Parent/Child(%)'])
    
    # List
    n_of_crystals_ = [0]
    num_image = []

    
    if island:   
        main_island(FOLDER_PATH, 5) # crop the island from micro type images
         
            
    print('Start to classify the crystals')
    files = get_files(FOLDER_PATH) 
    for file in files:
        properties = get_properties(file)
        
        if images_to_verify(properties, island):
            image = get_image(FOLDER_PATH, file)
            
            if properties[1] in images_to_crop(island):
                image = crop_the_image(image, scale_crop)

            status = status_color_image(image)
            
            if status == "Imagem com Fundo Escuro e Cristais Claros":
                contours, hierarchy, status_crystals = filter_nucleated_crystals(image)
                data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties, status_crystals)
            elif status == "Imagem com Fundo Claro e Cristais Escuros":
                contours, hierarchy, status_crystals = filter_non_nucleated_crystals(image)
                data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties, status_crystals)                
            elif status == "Imagem com Tons Médios":
                for filter_ in [filter_non_nucleated_crystals(image), filter_nucleated_crystals(image)]:
                    contours, hierarchy, status_crystals = filter_
                    data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties, status_crystals)
            
            # contours, hierarchy = filter(image, properties, status)
            # data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties, status)
            # for filter_ in [filter_non_nucleated_crystals(image), filter_nucleated_crystals(image)]:
            #     contours, hierarchy, status = filter_
            #     data, n_of_crystals, perct_parent, perct_child, perct_else  = classification(image, data, contours, hierarchy, properties, status)

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
    
    # print(hierarchy_erro())
    
    return data, data_crystals

if __name__ == '__main__':
    data, data_crystals = main(island=True, scale_crop=0.5)

# delete_islands(FOLDER_PATH)