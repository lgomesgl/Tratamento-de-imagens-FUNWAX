'''
    Graphics in readme.md
'''
import matplotlib.pyplot as plt
import seaborn as sns

def graphics(data, data_crystals):
    # 1: AR x Reynolds, hue = Type
    plt.subplot(2, 2, 1)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Type'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('AR x Reynolds')

    # 2: AR x Reynolds, hue = Toil
    plt.subplot(2, 2, 2)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Toil'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('AR x Reynolds')

    # 3: AR x Reynolds, hue = Tcool
    plt.subplot(2, 2, 3)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Tcool'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('AR x Reynolds')
 
    # 4: AR x Time
    plt.subplot(2, 2, 4)
    df = data.copy()
    df['Time'] = df['Time'].astype(int)
    df = df.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df, x=df['Time'], y=df['AR'], hue=df['Type'])
    plt.xlabel('Time [s]', fontweight='bold')
    plt.ylabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('AR x Time')
    plt.show()
    
    # 5: Distribution of AR
    sns.histplot(data, x = data['AR'], bins=50, kde=True, hue=data['Type'])
    plt.xlabel('Aspect ratio [-]', fontweight='bold')
    
    # plt.title('Distribution of AR')
    plt.show()
  
    # 6: Distribution of AR by Reynolds at Macro crystals
    plt.subplot(1,2,1)
    df_macro = data[(data['Type'] == 'Macro')]
    sns.histplot(df_macro, x = df_macro['AR'], bins=20, kde=True, hue=df_macro['Reynolds'])
    plt.xlabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('Distribution of AR by Reynolds at Macro crystals')
    
    # 7: Distribution of AR by Reynolds at Micro crystals
    plt.subplot(1,2,2)
    df_micro = data[(data['Type'] == 'Micro')]
    sns.histplot(df_micro, x = df_micro['AR'], bins=20, kde=True, hue=df_micro['Reynolds'])
    plt.xlabel('Aspect ratio [-]', fontweight='bold')
    # plt.title('Distribution of AR by Reynolds at Micro crystals')
    plt.show()
    # --------------------------------------- N_of_crystals graphics ---------------------------------------------------
    # 8: N of crystals x Reynolds, hue = Type
    df_1 = data_crystals.groupby(['Type','Reynolds'], as_index=False)['N_of_crystals'].sum()
    plt.subplot(2, 2, 1)
    sns.lineplot(x=df_1['Reynolds'], y=df_1['N_of_crystals'], hue=df_1['Type'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Number of crystals [-]', fontweight='bold')
    # plt.title('N_of_crystals x Reynolds')
 
    # 9: N of crystals x Reynolds, hue = Toil
    df_2 = data_crystals.groupby(['Toil','Reynolds'], as_index=False)['N_of_crystals'].sum()
    plt.subplot(2, 2, 2)
    sns.lineplot(x=df_2['Reynolds'], y=df_2['N_of_crystals'], hue=df_2['Toil'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Number of crystals [-]', fontweight='bold')
    # plt.title('N_of_crystals x Reynolds')
 
    # 10: N of crystals x Reynolds, hue = Tcool
    df_3 = data_crystals.groupby(['Tcool','Reynolds'], as_index=False)['N_of_crystals'].sum()
    plt.subplot(2, 2, 3)
    sns.lineplot(x=df_3['Reynolds'], y=df_3['N_of_crystals'], hue=df_3['Tcool'])
    plt.xlabel('Reynolds [-]', fontweight='bold')
    plt.ylabel('Number of crystals [-]', fontweight='bold')
    # plt.title('N_of_crystals x Reynolds')
 
    # 11: N_of_crystals x Time
    data_crystals['Time'] = data_crystals['Time'].astype(int)
    df_4 = data_crystals.groupby(['Type','Time'], as_index=False)['N_of_crystals'].sum()
    plt.subplot(2, 2, 4)
    # df_4 = df_4.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df_4, x=df_4['Time'], y=df_4['N_of_crystals'], hue=df_4['Type'])
    plt.xlabel('Time [s]', fontweight='bold')
    plt.ylabel('Number of crystals [-]', fontweight='bold')
    # plt.title('N_of_crystals x Time')
    plt.show()
    
    # # 12: Distribution of N_of_crystals
    # sns.histplot(data_crystals, x = data_crystals['N_of_crystals'].sum(), bins=15, kde=True, hue=data_crystals['Type'])
    # plt.title('Distribuiton of N_of_crystals')
    # plt.show()  
    
def hierarchy(data):
    plt.subplot(2,2,1)
    sns.scatterplot(data=data, x='Parent(%)', y='Child(%)', hue='Type', style='Reynolds', palette="ch:s=.25,rot=-.25")

    plt.subplot(2,2,2)
    sns.scatterplot(data=data, x='Parent(%)', y='No Parent/Child(%)', hue='Type', style='Reynolds', palette="ch:s=.25,rot=-.25")

    plt.subplot(2,2,3)
    sns.scatterplot(data=data, x='Parent(%)', y='Child(%)', hue='Time')

    plt.subplot(2,2,4)
    sns.scatterplot(data=data, x='Parent(%)', y='No Parent/Child(%)', hue='Time')
    plt.show()