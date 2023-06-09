'''
    Graphics in readme.md
'''

import matplotlib.pyplot as plt
import seaborn as sns

def graphics(data, data_crystals):
    # 1: AR x Reynolds, hue = Type
    plt.subplot(2, 2, 1)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Type'])
    plt.title('AR x Reynolds')

    # 2: AR x Reynolds, hue = Toil
    plt.subplot(2, 2, 2)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Toil'])
    plt.title('AR x Reynolds')

    # 3: AR x Reynolds, hue = Tcool
    plt.subplot(2, 2, 3)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Tcool'])
    plt.title('AR x Reynolds')
 
    # 4: AR x Time
    plt.subplot(2, 2, 4)
    df = data.copy()
    df['Time'] = df['Time'].astype(int)
    df = df.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df, x=df['Time'], y=df['AR'], hue=df['Type'])
    plt.title('AR x Time')
    plt.show()
    
    # 5: Distribution of AR
    sns.histplot(data, x = data['AR'], bins=100, kde=True, hue=data['Type'])
    plt.title('Distribuiton of AR')
    plt.show()
  
    # --------------------------------------- N_of_crystals graphics ---------------------------------------------------
    # 6: N of crystals x Reynolds, hue = Type
    plt.subplot(2, 2, 1)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Type'])
    plt.title('N_of_crystals x Reynolds')
 
    # 7: N of crystals x Reynolds, hue = Toil
    plt.subplot(2, 2, 2)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Toil'])
    plt.title('N_of_crystals x Reynolds')
 
    # 8: N of crystals x Reynolds, hue = Tcool
    plt.subplot(2, 2, 3)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Tcool'])
    plt.title('N_of_crystals x Reynolds')
 
    # 10: N_of_crystals x Time
    plt.subplot(2, 2, 4)
    df_ = data_crystals.copy()
    df_['Time'] = df_['Time'].astype(int)
    df_ = df_.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df_, x=df_['Time'], y=df_['N_of_crystals'], hue=df_['Type'])
    plt.title('N_of_crystals x Time')
    plt.show()
    
    # 9: Distribution of N_of_crystals
    sns.histplot(data_crystals, x = data_crystals['N_of_crystals'], bins=15, kde=True, hue=data_crystals['Type'])
    plt.title('Distribuiton of N_of_crystals')
    plt.show()  