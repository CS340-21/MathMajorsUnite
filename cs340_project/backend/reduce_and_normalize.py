import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def get_reduction(df, col, tech, name):

    # Only want to include numerical data
    x = df.select_dtypes(include=np.number).to_numpy()
    y = list(df[col]) # Guaranteed that col is in dataframe

    if tech == 0: # PCA
        pca = PCA(n_components = 2)
        pca.fit(x)
        embed = pca.fit_transform(x)
        tname = 'PCA'

    elif tech == 1: # TSNE
        embed = TSNE(n_components = 2).fit_transform(x)
        tname = 'TSNE'
    else:
        return -1

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

    savepath = os.path.join(os.path.abspath('.'), 'media/media/plots', 
        '{}_{}_{}.png'.format(tname, name, col))

    fig.savefig(savepath, dpi=100)

    plt.close()

    # Return the filename where plot was saved

        
