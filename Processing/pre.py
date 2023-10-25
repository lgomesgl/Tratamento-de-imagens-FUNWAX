import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('D:\LUCAS\IC\FUNWAX\Results_crystals.csv')
data_crystals = pd.read_csv('D:\LUCAS\IC\FUNWAX\Results_number_of_crystals.csv')

sns.jointplot(data, x='Time', y='AR', hue='Type')
plt.show()