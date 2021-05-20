import Data as d
from ADetector import ADetector
from Visualizer import Visualizer
from Backpropagation import Backtesting
import Data as data

def RunBackTesting(TS_ID):
    dfds = d.GetTimeSeries(TS_ID)
    targets = dfds['target'].unique()

    for target in targets:
        titleName = TS_ID + '_' + target
        df = dfds[dfds['target']==target]

        #BackTesting
        back = Backtesting(df)
        back.RunBackpropagation(minPeriods=6,chartTitle=titleName, metric='AlgoChangeDetected')
        back.GenerateGIF(titleName=titleName)


def RunDetection(TS_ID):
    #Get Data
    dfds = d.GetTimeSeries(TS_ID)
    targets = dfds['target'].unique()

    #Delete Output Data for TS_ID
    d._deleteTimeSeriesOutput(TS_ID)
        
    #Run detection
    for target in targets:
        try:
            titleName = TS_ID + '_' + target
            df = dfds[dfds['target']==target]
            print(target)
            #Change Detection
            detector = ADetector(df)
            detector.Run()

            dfResults = detector.GetResults()
            dfResults['ts_id'] = TS_ID
            dfResults['target'] = target
            d.SaveResults(dfResults)

            visuals = Visualizer(dfResults,plt_ymin = min(df.y),plt_ymax = max(df.y))
            visuals.PlotChangePoints(Title=titleName, fileName=titleName)

        except Exception as ex:
            print("Error with {0}".format(TS_ID + " - " + target))



# Run model
if __name__ == '__main__':
    TIME_SERIES_IDS = data.GetTimeSeriesIDs()
    #TIME_SERIES_IDS = ['BOOKINGS_PHYS_WAIT_TIMES','BOOKINGS_MA_WAIT_TIMES','BOOKINGS_DAILY_ARRIVAL_WAIT_TIMES']
    #TIME_SERIES_IDS = ['PA_PAYORS_RX_PMPM']
    
    #TS_ID = 'ENS_ER_DISCHARGES'
    #TS_ID = 'PA_PAYORS_MEDEX_PMPM'
    #TIME_SERIES_IDS = ['BOOKINGS_DAILY_DEPARTMENT_NO_SHOW_RATE']
    #RunDetection(TS_ID='BOOKINGS_DAILY_DEPARTMENT_FILL_RATE')
    #RunBackTesting(TS_ID='BOOKINGS_DAILY_DEPARTMENT_FILL_RATE')


    for TS_ID in TIME_SERIES_IDS:
        print("Processing {0}".format(TS_ID))
        RunDetection(TS_ID)
        #RunBackTesting(TS_ID)

    #RunDetection(TS_ID)


