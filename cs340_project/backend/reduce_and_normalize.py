import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import io
import urllib, base64

def get_img(fig, dpi = 200):
    '''
    fig: Figure from Matplotlib
    fig, ax = plt.subplots()
    dpi: resolution of image
    '''
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png', dpi = dpi)
    buf.seek(0)
    string = base64.b64encode(buf.getvalue())
    myplot = string.decode('utf-8')
    buf.close()
    plt.clf()
    plt.close()

    return myplot

def get_reduction(df, col, tech, name):
    '''
    df: dataframe
    col: column
    tech: technique code (0 for PCA, 1 for TSNE, 2 for Histogram)
    name: filename
    '''

    # Only want to include numerical data
    x = df.select_dtypes(include=np.number).to_numpy()
    y = list(df[col]) # Guaranteed that col is in dataframe

    plt.switch_backend('AGG')

    if int(tech) == 0: # PCA
        pca = PCA(n_components = 2)
        pca.fit(x)
        embed = pca.fit_transform(x)
        tname = 'PCA'

    elif int(tech) == 1:
        embed = TSNE(n_components = 2).fit_transform(x)
        tname = 'TSNE'
        
    elif int(tech) == 2:
        # Histogram functionality
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Error check
            return None
       
        fig, ax = plt.subplots()
        df.hist(column=col, ax=ax)
        fig.set_size_inches(10, 8)
        return get_img(fig)

    # Partition into labels:
    each_lab = {yi:[] for yi in set(y)}
    for i in range(len(y)):
        each_lab[y[i]].append(embed[i])

    fig, ax = plt.subplots()

    for lab, data in each_lab.items():
        npd = np.array(data)
        ax.scatter(npd[:,0], npd[:,1], label = str(lab))

    ax.legend()
    fig.set_size_inches(10, 8)
    ax.set_title('{} of {} on {} labels'.format(tname, name, col))

    # Return decoded object
    return get_img(fig)

        
