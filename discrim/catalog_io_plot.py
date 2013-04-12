import os, h5py, string
import numpy as np
import matplotlib.pyplot as plt

def write_catalogs_hdf5(X, y, features, labels):

    X = np.vstack((eq_cat,blast_cat))
    n_eq, f_f = eq_cat.shape
    n_s, n_f =  X.shape
    y = np.ones(n_s)
    y[0:n_eq]=0

    f=h5py.File(filename,'w')
    X_data=f.create_dataset('X',data=X)
    y_data=f.create_dataset('y',data=y)
    X_data.attrs['features'] = string.join(features,',')
    y_data.attrs['earthquake'] = labels['earthquake']
    y_data.attrs['blast'] = labels['blast']
    f.close()

def read_catalogs_hdf5(filename):

    f=h5py.File(filename,'r')
    X=np.array(f['X'])
    y=np.array(f['y'])
    features = f['X'].attrs['features'].split(',')
    labels={}
    for key, value in f['y'].attrs.iteritems():
        labels[key] = value
    f.close()

    return X, y, features, labels


def plot_catalogs(X, y, features, labels, title, filename, ranges=None):

    eq_label = labels['earthquake']
    bl_label = labels['blast']

    eq_cat =    X[y == eq_label]
    blast_cat = X[y == bl_label]

    fig = plt.figure(figsize=(9.5, 4))
    ax1=fig.add_subplot(121, axisbg='lightgrey')
    ax2=fig.add_subplot(122, axisbg='lightgrey')
    #ax3=fig.add_subplot(223, axisbg='lightgrey')
    #ax4=fig.add_subplot(224, axisbg='lightgrey')

    x_eq, y_eq, t_eq, h_eq, d_eq, w_eq = np.hsplit(eq_cat,6)
    x_blast, y_blast, t_blast, h_blast, d_blast, w_blast = np.hsplit(blast_cat,6)

    w_eq = np.around(w_eq.flatten())
    d_eq = np.around(d_eq.flatten())
    w_blast = np.around(w_blast.flatten())
    d_blast = np.around(d_blast.flatten())


    ax1.scatter(eq_cat[w_eq==1,2],eq_cat[w_eq==1,3],marker='o', color='b', linewidths=(0,))
    ax1.scatter(eq_cat[w_eq==0,2],eq_cat[w_eq==0,3],marker='o', color='green', linewidths=(0,))
    ax1.scatter(eq_cat[d_eq==0,2],eq_cat[d_eq==0,3],marker='o', color='black', linewidths=(0,))
    ax1.scatter(blast_cat[w_blast==1,2],blast_cat[w_blast==1,3], marker='o',color='red',  linewidths=(0,))
    ax1.scatter(blast_cat[w_blast==0,2],blast_cat[w_blast==0,3], marker='o',color='yellow', linewidths=(0,))
    ax1.scatter(blast_cat[d_blast==0,2],blast_cat[d_blast==0,3], marker='o',color='cyan', linewidths=(0,))
    ax1.set_xlabel(features[2])
    ax1.set_ylabel(features[3])
    if ranges:
        ax1.set_xlim(ranges[0][2], ranges[1][2])
        ax1.set_ylim(ranges[0][3], ranges[1][3])

    #ax2.plot(eq_cat[w_eq==1,0],eq_cat[w_eq==1,3],'b.')
    #ax2.plot(eq_cat[w_eq==0,0],eq_cat[w_eq==0,3],'g.')
    #ax2.plot(eq_cat[d_eq==0,0],eq_cat[d_eq==0,3],'k.')
    #ax2.plot(blast_cat[w_blast==1,0],blast_cat[w_blast==1,3],'r.')
    #ax2.plot(blast_cat[w_blast==0,0],blast_cat[w_blast==0,3],'.',color='yellow')
    #ax2.plot(blast_cat[d_blast==0,0],blast_cat[d_blast==0,3],'.',color='cyan')
    #ax2.set_xlabel(features[0])
    #ax2.set_ylabel(features[3])

    #ax3.plot(eq_cat[w_eq==1,2],eq_cat[w_eq==1,1],'b.')
    #ax3.plot(eq_cat[w_eq==0,2],eq_cat[w_eq==0,1],'g.')
    #ax3.plot(eq_cat[d_eq==0,2],eq_cat[d_eq==0,1],'k.')
    #ax3.plot(blast_cat[w_blast==1,2],blast_cat[w_blast==1,1],'r.')
    #ax3.plot(blast_cat[w_blast==0,2],blast_cat[w_blast==0,1],'.',color='yellow')
    #ax3.plot(blast_cat[d_blast==0,2],blast_cat[d_blast==0,1],'.',color='cyan')
    #ax3.set_xlabel(features[2])
    #ax3.set_ylabel(features[1])

    ax2.scatter(eq_cat[w_eq==1,0],eq_cat[w_eq==1,1], marker='o', color='b', linewidths=(0,))
    ax2.scatter(eq_cat[w_eq==0,0],eq_cat[w_eq==0,1],marker='o',color='green', linewidths=(0,))
    ax2.scatter(eq_cat[d_eq==0,0],eq_cat[d_eq==0,1],marker='o',color='black', linewidths=(0,))
    ax2.scatter(blast_cat[w_blast==1,0],blast_cat[w_blast==1,1],marker='o', color='red', linewidths=(0,))
    ax2.scatter(blast_cat[w_blast==0,0],blast_cat[w_blast==0,1],marker='o',color='yellow', linewidths=(0,))
    ax2.scatter(blast_cat[d_blast==0,0],blast_cat[d_blast==0,1],marker='o',color='cyan', linewidths=(0,))
    ax2.set_xlabel(features[0])
    ax2.set_ylabel(features[1])
    if ranges:
        ax2.set_xlim(ranges[0][0], ranges[1][1])
        ax2.set_ylim(ranges[0][0], ranges[1][1])

    fig.subplots_adjust(hspace=4)

    plt.suptitle(title, fontsize=16)

    #plt.show()
    plt.savefig(filename)
    plt.clf()


def plot_prob(X, X_prob, features, labels, title, filename, ranges=None):

    fig = plt.figure(figsize=(9.5, 4))
    ax1=fig.add_subplot(121, axisbg='lightgrey')
    ax2=fig.add_subplot(122, axisbg='lightgrey')
    #ax3=fig.add_subplot(223, axisbg='lightgrey')
    #ax4=fig.add_subplot(224, axisbg='lightgrey')

    x, y, t, h, d, w = np.hsplit(X,6)
    prob=np.max(X_prob, axis=1)

    w = np.around(w.flatten())
    d = np.around(d.flatten())


    ax1.scatter(t.flatten(),h.flatten(),c=prob, marker='o', linewidths=(0,), cmap='afmhot')
    ax1.set_xlabel(features[2])
    ax1.set_ylabel(features[3])
    if ranges:
        ax1.set_xlim(ranges[0][2], ranges[1][2])
        ax1.set_ylim(ranges[0][3], ranges[1][3])

    cs=ax2.scatter(x.flatten(),y.flatten(),c=prob, marker='o', linewidths=(0,), cmap='afmhot')
    ax2.set_xlabel(features[0])
    ax2.set_ylabel(features[1])
    if ranges:
        ax2.set_xlim(ranges[0][0], ranges[1][1])
        ax2.set_ylim(ranges[0][0], ranges[1][1])

    fig.colorbar(cs, ax=ax2, shrink=0.9)
    fig.subplots_adjust(hspace=4)

    plt.suptitle(title, fontsize=16)

    #plt.show()
    plt.savefig(filename)
    plt.clf()
