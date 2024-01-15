import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def dist_image(df):
    try:
        plt.subplot(1,2,1)
        sns.histplot(df, x = df['AR'], bins=20, kde=True)
        plt.title('Normal Distribuiton of AR')
        
        plt.subplot(1,2,2)
        sns.histplot(df, x = df['AR'], bins=20, kde=True, weights=df['AR']) 
        plt.title('Weighted Distribuiton of AR')
        plt.show()
    except:
        pass