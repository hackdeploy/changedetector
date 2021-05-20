import pandas as pd
import numpy as np
import ruptures as rpt
import Detectors as detect


class ADetector:

    def __init__(self, ds):
        self.ds = ds[['ds','y']].sort_values(by='ds', ascending=True)

        #for adtk
        self.dfI = self.ds[['ds','y']]
        self.dfI = self.dfI.sort_values(by='ds', ascending=True)
        self.dfI['ds'] = pd.to_datetime(self.dfI['ds'])
        self.dfI.index = pd.to_datetime(self.dfI['ds'])
        self.dfI= self.dfI.drop(columns=['ds'])
        
        #output
        self.dates = ds['ds'].values
        self.y = ds['y'].values
        self.levelChanges = []
        self.changepointChanges = []
        self.outliers = []
        self.outliers_robust = []

    def Run(self):
        try:
            #self._detectLevelChanges()
            self._detectChangePoints()
            self._detectOutliers()
            self._detectOutliersRobust()

        except:
            print("Error")

    def GetResults(self):
        # dictionary of lists  
        d = {
              'ds': self.dates
             ,'y': self.y
             ,'AlgoChangeDetected':self.changepointChanges
             ,'AlgoOutlierDetected':self.outliers
             ,'AlgoOutlierDetectedRobust':self.outliers_robust
             #,'AlgoLevelChange': self.levelChanges
             } 
        return pd.DataFrame(d)

    def _detectLevelChanges(self):
        from adtk.data import validate_series
        from adtk.detector import LevelShiftAD

        level_shift_ad = LevelShiftAD(c=5.0, side='both', window=7)
        anomalies = level_shift_ad.fit_detect(self.dfI)
        #anomalies = anomalies.fillna(0)
        self.levelChanges = anomalies.y.values

    def _detectChangePoints(self):
        model="rbf"
        isChangeDetected=True
        for pen in reversed(range(2, 7, 1)):
            algo = rpt.Pelt(model=model).fit(self.ds.y.values)
            result = algo.predict(pen=pen)
            if (len(result)>0) or (p<=3):
                break
                isChangeDetected=False

        #get results
        algoChangeDetected = np.zeros(self.ds.shape[0])
        for i, idx in enumerate(result):
            if i!=len(result)-1:#ignore the last change detected.
                algoChangeDetected[idx-1] = 1

        self.changepointChanges = algoChangeDetected

    def _detectOutliersRobust(self):
        threshold=2
        result = detect.OutlierSignalDetection_RobustZScore(self.ds.y.values, threshold=threshold)
        self.outliers_robust = result


    def _detectOutliers(self):
        lag=5
        threshold=3
        influence=.4
        result = detect.OutlierSignalDetection_ZScoreFiltered(self.ds.y.values, lag=lag, threshold=threshold, influence=influence)
        self.outliers = result['signals']



        

