#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
import glob

filelist = glob.glob("*csv")
params = [] # list to store parameters
for f in filelist:
    # read data
    data = np.loadtxt(f, delimiter="\t",
                    usecols=[0,1,2])

    # Z = 1/j w C, log for Z and f for polynomial fitting
    logfz = np.log(data[:,0:2])

    # fitting
    p = P.polyfit(logfz[:,0], logfz[:,1], 1)
    fitz = np.exp(p[0] + p[1] * logfz[:,0])

    # save parameter
    #np.savetxt(f"{f}param.csv", p, delimiter="\t") # save file name using original file
    params.append([[f, p]]) # append file name and parameters to the storage

    # plot
    fig, ax = plt.subplots()
    ax.plot(data[:,0], data[:,1], color="b")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax2 = ax.twinx()
    ax2.plot(data[:,0], data[:,2], color="g")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|Z| ($\Omega$)", color="b")
    ax2.set_ylabel("$\phi$ (deg)", color="g")
    ax2.set_ylim((-90, 0))
    ax.plot(data[:,0], fitz, color="r")
    plt.show()
    plt.savefig(f"{f}plot.png")

np.savetxt("params.csv", params, delimiter="\t")