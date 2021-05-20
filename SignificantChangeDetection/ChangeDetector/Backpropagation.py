import pandas as pd

from ADetector import ADetector
from Visualizer import Visualizer


import os
from os import listdir
from os.path import isfile, join
import glob

class Backtesting():

    def __init__(self, df):
        self.df = df
        self.df = self.df.sort_values(by='ds', ascending=True)

        files = glob.glob('C:/MYLOCALFILES/WORKSPACES/RD_PROJECTS/SignificantChangeDetection/ChangeDetector/seqimg/*.*')
        for f in files:
            os.remove(f)

    def RunBackpropagation(self, minPeriods=30, chartTitle="Trend", metric='AlgoOutlierDetected'):
        AS_OF_DATES = self.df['ds'].unique()

        for i, toDate in enumerate(AS_OF_DATES):
            print(toDate)
            dfSource = self.df[self.df['ds']<=toDate]

            #need at least 10 records to run model
            if dfSource.shape[0]>minPeriods:
                detector = ADetector(dfSource)
                detector.Run()

                dfResults = detector.GetResults()
                dfResults['AsOfDate'] = toDate

                #Prepare for Visualization (including future dates with 0's)
                xDates = self.df['ds'].values
                y = list(dfResults['y'].values)
                changepointChanges = list(dfResults[metric].values)
                while len(y)<len(xDates):
                    y.append(0)
                    changepointChanges.append(0)
                
                d = {
                    'ds': xDates
                     ,'y': y
                    ,metric:changepointChanges
                } 

                dfResultsCharting = pd.DataFrame(d)

                #Save Image
                visuals = Visualizer(dfResultsCharting,plt_ymin = min(self.df.y),plt_ymax = max(self.df.y))
                visuals.PlotChangePoints(Title=chartTitle,fileName=str(i),folderName="seqimg", metric=metric)



    def GenerateGIF(self, titleName = 'detectionSim'):
        import imageio
        path = 'C:/MYLOCALFILES/WORKSPACES/RD_PROJECTS/SignificantChangeDetection/ChangeDetector/seqimg'
        filenames = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('./gif/{0}.gif'.format(titleName), images)

        

