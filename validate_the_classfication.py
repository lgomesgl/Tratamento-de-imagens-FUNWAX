'''
    Take each crystal that the script crystal_images.py has classify and do the classify manually
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from cristal_class import CrystalsClassification
from classification_crystals import NAME_CSV_FILE

# FOLDER_PATH = '/home/lucas/FUNWAX/Images'
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'

def read_data():
    return pd.read_csv(NAME_CSV_FILE)







