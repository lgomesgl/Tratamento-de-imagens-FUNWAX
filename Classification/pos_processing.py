'''
    Graphics in readme.md
'''

import matplotlib.pyplot as plt
import seaborn as sns

def graphics(data):
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
    # # 6: N of crystals x Reynolds, hue = Type
    # df_1 = data_crystals.groupby(['Type','Reynolds'], as_index=False)['N_of_crystals'].sum()
    # plt.subplot(2, 2, 1)
    # sns.lineplot(x=df_1['Reynolds'], y=df_1['N_of_crystals'], hue=df_1['Type'])
    # plt.title('N_of_crystals x Reynolds')
 
    # # 7: N of crystals x Reynolds, hue = Toil
    # df_2 = data_crystals.groupby(['Toil','Reynolds'], as_index=False)['N_of_crystals'].sum()
    # plt.subplot(2, 2, 2)
    # sns.lineplot(x=df_2['Reynolds'], y=df_2['N_of_crystals'], hue=df_2['Toil'])
    # plt.title('N_of_crystals x Reynolds')
 
    # # 8: N of crystals x Reynolds, hue = Tcool
    # df_3 = data_crystals.groupby(['Tcool','Reynolds'], as_index=False)['N_of_crystals'].sum()
    # plt.subplot(2, 2, 3)
    # sns.lineplot(x=df_3['Reynolds'], y=df_3['N_of_crystals'], hue=df_3['Tcool'])
    # plt.title('N_of_crystals x Reynolds')
 
    # # 9: N_of_crystals x Time
    # df_4 = data_crystals.groupby(['Type','Time'], as_index=False)['N_of_crystals'].sum()
    # plt.subplot(2, 2, 4)
    # df_4['Time'] = df_4['Time'].astype(int)
    # df_4 = df_4.sort_values('Time', ascending=True).reset_index(drop=True)
    # sns.lineplot(df_4, x=df_4['Time'], y=df_4['N_of_crystals'], hue=df_4['Type'])
    # plt.title('N_of_crystals x Time')
    # plt.show()
    
    # # 10: Distribution of N_of_crystals
    # sns.histplot(data_crystals, x = data_crystals['N_of_crystals'].sum(), bins=15, kde=True, hue=data_crystals['Type'])
    # plt.title('Distribuiton of N_of_crystals')
    # plt.show()  