from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np

class Visualizer():

    def __init__(self, df, plt_ymin,plt_ymax):
        self.df = df
        self.imageFileName = ''
        self.plt_ymin = plt_ymin
        self.plt_ymax = plt_ymax

    def PlotChangePoints(self, Title="", fileName="img", folderName="img"):
        try:
            fig=figure(num=None, figsize=(15, 5))
            
            plt.plot(self.df['ds'], self.df['y'], '-', color='black');

            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Value', fontsize=12)
            plt.title(Title,fontdict = {'fontsize' : 16})
            plt.ylim(self.plt_ymin, self.plt_ymax)

            #plot changepoints
            change_point_metric = 'AlgoChangeDetected'
            pos_changePoints = self.df[self.df[change_point_metric] >0].values
            neg_changePoints = self.df[self.df[change_point_metric] <0].values

            for i, ds in enumerate(self.df['ds'].values):
                #ds2 = date.strftime(ds, "%m/%d/%Y")
                if ds in pos_changePoints:
                    plt.axvline(ds,ls='--', lw=2,color='grey')
                if ds in neg_changePoints:
                    plt.axvline(ds,ls='--', lw=2,color='grey')

            #plot outliers
            outlier_metrc  = 'AlgoOutlierDetected'

            index_changes = self.df[self.df[outlier_metrc] >0].index
            plt.scatter(self.df.iloc[index_changes].ds, self.df.iloc[index_changes].y, c='green', label="outlier")
            index_changes = self.df[self.df[outlier_metrc] <0].index
            plt.scatter(self.df.iloc[index_changes].ds, self.df.iloc[index_changes].y, c='red', label="outlier")

            #save image
            self.imageFileName = '{0}.png'.format(fileName)
            fig.savefig("./{0}/{1}".format(folderName,self.imageFileName))
            plt.close(fig)
            #plt.show()

        except Exception as ex:
            print("Error with " + Title)