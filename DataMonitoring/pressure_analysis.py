import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep
import os
from scipy import signal
from scipy.signal import savgol_filter
from scipy.signal import lfilter

#first test
waterflowData = pd.read_csv(os.getcwd() + "/data/WaterFlowTest_08_08_16_42")
tankData = waterflowData['low2'].to_numpy()
amountOfData = len(tankData)
currPressureData = np.asarray([0] * amountOfData)

#second test
waterflowData2 = pd.read_csv(os.getcwd() + "/data/waterflow_test_full_9_5_16_16")
tankData2 = waterflowData2['low1'].to_numpy()
amountOfData2 = len(tankData2)
currPressureData2 = np.asarray([0] * amountOfData2)

#third test
waterflowData3 = pd.read_csv(os.getcwd() + "/data/waterflow_test_full_9_5_14_31 (1)")
tankData3 = waterflowData3['low1'].to_numpy()
amountOfData3 = len(tankData3)
currPressureData3 = np.asarray([0] * amountOfData3)

#function for detecting peaks in data
##example: detect2(tankData)
def detect2(data):
    xaxis = np.arange(0,len(data),1)
    print("Amount of Data Points:", len(data))
    n = 5  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1
    yyy = lfilter(b,a,data)
    dary = np.array([*map(float, data)])
    dary -=np.average(dary)
    step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))

    dary_step = np.convolve(dary, step, mode='valid')
    peaksall=[]
    peaks = signal.find_peaks(dary_step, width=20)[0]
    if len(peaks)>0:
        peaksall.append(peaks)
    print("Positive Peaks:", len(peaks))
    peaks2 = signal.find_peaks(-dary_step, width=20)[0]
    print("Negative Peaks:", len(peaks2))
    if len(peaks2)>0:
        peaksall.append(peaks2)
    print("Total Peaks detected:", len(peaksall))
    print(peaksall)
    plt.figure()

    plt.plot(dary)

    plt.plot(dary_step/10)

    for ii in range(len(peaks)):
        plt.plot((peaks[ii], peaks[ii]), (-1500, 1500), 'r')

    plt.show()
    
    if len(peaksall)>=2:
        data2 = data[int(peaksall[0][0]):int(peaksall[-1][-1])]
    else:
        data2 = data[0:int(peaksall[-1])]
    ##
    n = 5  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1
    yy = lfilter(b,a,data2)
    ##
    dary2 = np.array([*map(float, data2)])
    
    dary2 -=np.average(dary2)
    step2 = np.hstack((np.ones(len(dary2)), -1*np.ones(len(dary2))))

    dary_step2 = np.convolve(dary2, step2, mode='valid')

    # Get the peaks of the convolution
    #negative peaks
    peaks3 = signal.find_peaks(-dary_step2, width=20)[0]
    #positive peaks
    peaks4 = signal.find_peaks(dary_step2, width=20)[0]
    #adjusting for frame shift
    if len(peaksall)>=2:
        if len(peaks3)>0:
            peaksall.append(peaks3+peaks+1)
        print("Negative Peaks Detected:", len(peaks3), "at", peaks3)
        if len(peaks4)>0:
            peaksall.append(peaks4+peaks+1)
        print("Positive Peaks Detected:", len(peaks4), "at", peaks4)
        print(peaksall)
    else:
        if len(peaks3)>0:
            peaksall.append(peaks3)
        print("Negative Peaks Detected:", len(peaks3),"at",peaks3)
        if len(peaks4)>0:
            peaksall.append(peaks4)
        print("Positive Peaks Detected:", len(peaks4),"at", peaks4)
        print(peaksall)
    ###make this more robust
    #peaks2 = signal.find_peaks(-dary_step, width=20)[0]
    print(peaks3)

    # plots
    plt.figure()

    plt.plot(dary2)
    #orange:
    plt.plot(dary_step2/10)
    #repeat process on dary data:
    n = 20  # the larger n is, the smoother curve will be
    b = [1.0 / n] * n
    a = 1
    yyyy = lfilter(b,a,dary_step2/10)
    peaks40 = signal.find_peaks(yyyy, width=20)[0]
    peaks30 = signal.find_peaks(-yyyy, width=20)[0]
    peaksall2=[]
    plt.plot(yyyy)
    for ii in range(len(peaks40)):
        plt.plot((peaks40[ii], peaks40[ii]), (-150, 150), 'green')
    ##adding to master graph
    if len(peaksall)>=2:
        if len(peaks30)>0:
            peaksall2.append(peaks30+peaks+1)
        print("Negative Peaks Detected:", len(peaks30), "at", peaks30)
        if len(peaks40)>0:
            peaksall2.append(peaks40+peaks+1)
        print("Positive Peaks Detected:", len(peaks40), "at", peaks40)
        print(peaksall2)
    else:
        if len(peaks30)>0:
            peaksall2.append(peaks30)
        print("Negative Peaks Detected:", len(peaks30),"at",peaks30)
        if len(peaks40)>0:
            peaksall2.append(peaks40)
        print("Positive Peaks Detected:", len(peaks40),"at", peaks40)
        print(peaksall2)
    ##   
        
    for ii in range(len(peaks3)):
        plt.plot((peaks3[ii], peaks3[ii]), (-150, 150), 'r')

    
    plt.show()

    plt.figure(dpi=150)
    plt.plot(xaxis, data)
    print(peaksall)
    for i in peaksall:
        for x in i:
            plt.axvline(x,c='k', lw='1')
    
    for i in peaksall2:
        for x in i:
            plt.axvline(x,c='green', lw='1')
            
            



