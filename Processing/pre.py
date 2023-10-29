import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('D:\LUCAS\IC\FUNWAX\Results_crystals.csv')
data_crystals = pd.read_csv('D:\LUCAS\IC\FUNWAX\Results_number_of_crystals.csv')

plt.subplot(2,2,1)
sns.scatterplot(data=data_crystals, x='Parent(%)', y='Child(%)', hue='Type', style='Reynolds', palette="ch:s=.25,rot=-.25")

plt.subplot(2,2,2)
sns.scatterplot(data=data_crystals, x='Parent(%)', y='No Parent/Child(%)', hue='Type', style='Reynolds', palette="ch:s=.25,rot=-.25")

plt.subplot(2,2,3)
sns.scatterplot(data=data_crystals, x='Parent(%)', y='Child(%)', hue='Time')

plt.subplot(2,2,4)
sns.scatterplot(data=data_crystals, x='Parent(%)', y='No Parent/Child(%)', hue='Time')
plt.show()