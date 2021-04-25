import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

import io
import urllib, base64

def get_reduction(df, col, tech, name):

    # Only want to include numerical data
    x = df.select_dtypes(include=np.number).to_numpy()
    y = list(df[col]) # Guaranteed that col is in dataframe

    if int(tech) == 0: # PCA
        pca = PCA(n_components = 2)
        pca.fit(x)
        embed = pca.fit_transform(x)
        tname = 'PCA'

    # elif tech == 1: # TSNE
    elif int(tech) == 1:
        embed = TSNE(n_components = 2).fit_transform(x)
        tname = 'TSNE'
    # else:
    #     return -1]

    plt.switch_backend('AGG')

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

    buf = io.BytesIO()
    # buf = io.StringIO()
    fig.savefig(buf, format = 'png', dpi = 150)
    buf.seek(0)
    string = base64.b64encode(buf.getvalue())
    myplot = string.decode('utf-8')
    buf.close()
    plt.clf()
    plt.close()

    # Return decoded object
    return myplot

        
