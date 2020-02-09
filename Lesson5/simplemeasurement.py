# -*- coding: utf-8 -*-
import visa
import numpy as np
import sys
import matplotlib.pyplot as plt

# sweep parameters
base = 20.
sweepstart = 1. # frequency sweep from base**sweepstart
sweepstop = 5.6 # frequency sweep end at base**sweepstop
numberOfPoints = 101
fillMode = "log" # parameter steps. linear or log
amp = 0.1 # voltage amplitude
averaging = 1 # number of averaging
bias = 0 # dc bias
aperture = "MED" # measurement time
correction_open = "OFF" # open correction status

# timeout for sweep(s) in second
timeout = 300

def measurement(pia, basefname):
    pia.timeout = 1000000 # timeout in milisecond
    pia.write(":DISP:CCL") # clear error message
    pia.write(":TRIG:SOUR BUS") # trigger mode BUS mode from USB
    pia.write("*CLS") # clear messages

    # setup measurement parameters
    pia.write(":FUNC:IMP:TYPE ZTD") # sets maeasurement function to Z-thd
    pia.write(":FUNC:IMP:RANG:AUTO ON") # automatic measurement range

    # make sweep parameter list
    if fillMode == "log":
        sweepList = np.logspace(sweepstart, sweepstop, num=numberOfPoints)
    else:
        sweepList = np.linspace(sweepstart, sweepstop, num=numberOfPoints)
    sweepListString = ",".join(map(lambda x: f"{x:.8e}", sweepList))
    pia.write(f":LIST:FREQ {sweepListString}") # sweep parameter to frequency
    pia.write(":LIST:MODE SEQ") # sweep mode list, sequential
    pia.write(":DISP:PAGE LIST") # shows list display

    pia.write(f":APER {aperture}, {averaging}") # measurement time medium

    pia.write(f":VOLT {amp}") # oscillator mode to votage 0.1 V
    pia.write(":BIAS:STAT OFF")# DC bias off :BIAS:STAT?

    pia.write(":SYST:BEEP:STAT ON") # enables beep
    pia.write(":COMP:BEEP PASS") # beeps when measurement passes: default fail

    pia.write(f":CORR:OPEN:STAT {correction_open}") # open correction

    pia.write(":STAT:OPER:ENAB 0")
    pia.write(":ABOR;:INIT")

    pia.write(":TRIG") # trigger measurement
    pia.write("*WAI") # wait until finishes

    print(pia.query(":SYST:ERR?")) # show system error if any

    sweepParamList = np.array(pia.query_ascii_values(":LIST:FREQ?")) # returns parameter list query
    swp = np.array(sweepParamList.reshape((len(sweepParamList), 1))) # reshape parameter list
    result = np.array(pia.query_ascii_values('FETC?')) # result
    res2 = np.reshape(result, (len(result)/4,4)) # reshape result
    allresult = np.hstack((swp, res2)) # merge freq and result

    # save data
    tab = "\t"
    header = f"""\
data file made from Agilent E4980A Precision LCR Meter by simplemeasurement.py
Measurement mode = {pia.query(':FUNC:IMP?').strip()}
Osc Level = {pia.query(':VOLT?').strip()}
DC Bias State = {pia.query(':BIAS:STAT?').strip()}
DC Bias Level = {pia.query(':BIAS:VOLT?').strip()}
Averaging = {pia.query(':APER?').strip()}
Sweep Mode = {pia.query(':LIST:MODE?').strip()}
Open Correction = {pia.query(':CORR:OPEN:STAT?').strip()}
Freqency{tab}Z{tab}phi"""
    np.savetxt(f"{basefname}.csv", allresult, delimiter='\t', header=header)

    # after measurement, change display format
    pia.write(":TRIG:SOUR INT") # change to internal (continuous) trigger
    pia.write(":LIST:FREQ 1000")
    pia.write(":DISP:PAGE MEAS") # shows measurement display
    #pia.write(":FUNC:IMP CPD") # shows C-PD
    pia.write(":FREQ 1000")
    return allresult

def plotResult(data, fname):
    # data consists of freq, Z, phi (deg)
    fig, ax = plt.subplots()
    ax.set_xlabel("Freqency (Hz)")
    ax.set_ylabel("|Z|", color="b")
    ax.tick_params(axis="y",colors="b")
    ax.set_xscale('log')
    ax.set_yscale("log")
    ax.plot(data[:,0], data[:,1], ".") # plot
    ax2 = ax.twinx()
    ax2.set_ylim(-90, 90)
    ax2.set_ylabel('Phase', color="r", zorder=1)
    ax2.set_xticks([])
    ax2.tick_params(axis="y",colors="r")
    ax2.semilogx(data[:,0], data[:,2], '.', color="r") #phi
    ax.get_xaxis().get_major_formatter().labelOnlyBase = False

    plt.show()
    fig.savefig(fname+"plot.png")
    plt.clf()

def main():
    # read save file name from command line option
    if len(sys.argv) < 2:
        print('input file name to save')
        return 0
    else:
        basefname = sys.argv[1]

    # open instrument
    rm = visa.ResourceManager("C:/Windows/System32/visa64.dll")
    pia = rm.open_resource('USB0::0x0957::0x0909::MY46204132::0::INSTR')

    # run measurement
    result = measurement(pia, basefname)

    # plot result
    plotResult(result, f"{basefname}.png")

main()