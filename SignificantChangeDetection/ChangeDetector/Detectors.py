import numpy as np

def OutlierSignalDetection_ZScoreFiltered(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = np.zeros(len(y))
    stdFilter = np.zeros(len(y))
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))



def OutlierSignalDetection_RobustZScore(y, threshold):
    signals = np.zeros(len(y))
    
    #need at least 3 points to calculate. Set range to begin at 4.
    for i in range(4,len(y)):
        idx_window_start = 0
        idx_window_end = i
        
        y_window = y[idx_window_start:idx_window_end]
        
        #begin outlier calculation
        
        #calculate median without last value as the last value will be analyzed for outlier.
        median = np.median(y_window[:-1])
        d = abs(y_window-median)
        MAD = np.median(d)
        Mi = (0.6745*(y_window-median))/MAD
        
        #get the last item's score
        lastPointScore = Mi[i-1]
        
        if lastPointScore>threshold:
            signals[i-1] = 1
        if lastPointScore<-threshold:
            signals[i-1] = -1
        
        if 1==0:
            print(i+1,idx_window_start,idx_window_end,median,y[i],Mi[i-1])
            print(y_window)
            print(Mi)        
            print(signals)    
            #median = np.median(filteredY[(i-lag+1):i+1])

    return signals



def OutlierSignalDetection_RobustZScore_NOWINDOW(y, threshold):
    y_window = y
    median = np.median(y_window)

    d = abs(y_window-median)
    MAD = np.median(d)

    Mi = (0.6745*(y_window-median))/MAD

    signals = np.zeros(len(y_window))
    for i, v in enumerate(Mi):
        if v>=threshold:
            signals[i]=1
        if v<=-threshold:
            signals[i]=-1
        
    return signals
