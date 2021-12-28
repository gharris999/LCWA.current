'''
Created on Apr 16, 2020

@author: klein

class to plot the speedtest results
is called by test_speed3
'''

import matplotlib.pyplot as plt
import matplotlib.dates as md

import datetime
import numpy as np
import csv
import time
import sys
import os.path
import dropbox



class MyPlot(object):
    '''
    classdocs
    '''


    def __init__(self, path , filename , token , PlotFlag):
        '''
        Constructor
        file: is the speedtest filename
        token: is the dropbox file
        '''
        
        
        
        # First check for python version, this is important for the matlob read part
        self.MyPythonVersion()
        
        #now check if file is available, if not we exit
        
        file = path+'/'+filename
        
        if(self.IsFile(file)):
            self.InputFile = file
            self.output = self.InputFile.replace('csv','pdf')

        if(self.IsFile(token)):
            self.TokenFile = token
        
        self.dropbox_name = filename.replace('csv','pdf')
         
        self.path = path
        self.PlotFlag = PlotFlag    #Controls if there is a plot
         
        

    
    def MyPythonVersion(self):
        """ checks which version of python we are running
        """

        if (sys.version_info[0] == 3):
            print(' we have python 3')
            vers = True
        else:
            print(' you should switch to python 2')
            vers = False
        return vers

    
    
    
    def ReadFile(self):
        """ reads the csv file from the speedfile directory"""
        
        
        
        self.temp_name = self.path+'/temp.txt'
        self.temp_file = open(self.temp_name,'w')
        counter = 0
        for line in open(self.InputFile, 'r'):
            a = line.split(',')
            if(len(a)< 9):
                print ('problem',a)
                print ('ignore data point at line ',counter+1)
            else:
                self.temp_file.write(line)

            counter = counter+1
            

        self.temp_file.close()
        
    def ReadTestData(self,legend):
        """
        Reads the results with Matplotlib
        """
        
        self.ReadFile()
#        self.temp_file.seek(0)
        #f=open(self.temp_name,'rb')
        #f=open('/Users/klein/speedfiles/nuke_2020-04-17speedfile.csv') 
        
        self.legend = legend #legend is a dictionary'
        
        if(self.MyPythonVersion):
           
            x1,y1,y2 = np.loadtxt(self.temp_name, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: self.MyTime},skiprows = 1)
            
        else:
          
                  
            x1,y1,y2 = np.loadtxt(self.temp_name, delimiter=',',
                   unpack=True,usecols=(1,7,8),
                   converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2
        self.PlotTestData(x1, y1, y2)
         
    
    def PlotTestData(self,x1,y1,y2):
        """
        Plots the tests
        """
        np.set_printoptions(precision=2)
        fig=plt.figure() 
        ax=fig.add_subplot(1,1,1)
        
        #Add Ip address
        
        
        #ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
        #ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
        #ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)

        #add legend
        print(self.legend)
        ax.text(.05,.95,'MyIP = '+self.DigIP(),weight='bold',transform=ax.transAxes,fontsize=11)

        plt.plot_date(x1,y1,'bs',label='\n blue DOWN ')
        plt.plot_date(x1,y2,'g^',label=' green UP')
        #plt.text(1.,1.,r' $\sigma = .1$')
        plt.grid(True)

        ax.xaxis.set_major_locator(md.MinuteLocator(interval=60))
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        plt.xlabel('Time')
        plt.ylabel('Speed in Mbs')

        plt.title('Speedtest LCWA '+self.InputFile)
    
        plt.legend(facecolor='ivory',loc="center left",shadow=True, fancybox=True)
        if(np.around(np.mean(y1),2) > 40.): #starlink
            plt.ylim(0.,60.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 40. and np.around(np.mean(y1),2) > 21.):
            plt.ylim(0.,41.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 21. and np.around(np.mean(y1),2) > 12.):
            plt.ylim(0.,24.) # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 12. and np.around(np.mean(y1),2) > 7.):
            plt.ylim(0.,12.) # set yaxis limit
             # set yaxis limit
        elif(np.around(np.mean(y1),2) <= 7. ):
            plt.ylim(0.,7.) # set yaxis limit

        
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        print('input file',self.InputFile)

        print (self.output)
        fig.savefig(self.output, bbox_inches='tight')
        if(self.PlotFlag):
            plt.show()  #Uncomment for seeing the plot



    
    
    def MyTime(self,b):
        """ conversion routine for time to be used in Matplotlib"""

        
        s=b.decode('ascii')
        
        a =md.date2num(datetime.datetime.strptime(s,'%H:%M:%S'))    
        
        return a
    
    

    def IsFile(self,filename):
        """checks if file exists"""
        
        try:
            os.path.isfile(filename)
            return True
        
        except:
            print('no file:   ' , filename)
            sys.exit(0)

    def ConnectDropbox(self):
        """
        here we establish connection to the dropbox account
        """
        #f=open(self.keyfile,"r")
        #self.key =f.readline() #key for encryption
        #self.key = pad(self.key,16)
        #f.close()

        f=open(self.TokenFile,"r")
        self.data =f.readline() #key for encryption
        

         
         
         
         #connect to dropbox 
        self.dbx=dropbox.Dropbox(self.data.strip('\n'))

        self.myaccount = self.dbx.users_get_current_account()
        print('***************************dropbox*******************\n\n\n')
        print( self.myaccount.name.surname , self.myaccount.name.given_name)
        print (self.myaccount.email)
        print('\n\n ***************************dropbox*******************\n')

    def DigIP(self):
        """ gets the ipaddress of the location"""
        
        stream = os.popen('dig +short myip.opendns.com @resolver1.opendns.com')
        return stream.read().strip('\n')
   
    
    
    def PushFileDropbox(self,dropdir):  
        f =open(self.output,"rb")

        self.dbx.files_upload(f.read(),dropdir+self.dropbox_name,mode=dropbox.files.WriteMode('overwrite', None))

       
if __name__ == '__main__':
    path = '/Users/klein/speedfiles'
    file = 'LC04_2021-12-28speedfile.csv'
    #file = 'test.csv'
    #file = 'LC01_2021-05-02speedfile.csv'
    token ='/Users/klein/git/LCWA/src/LCWA_d.txt'
    legend = {'IP':'63.233.221.150','Date':'more tests','Dropbox':'test', 'version':'5.01.01'}
    PlotFlag = True # flag to plot or not on screen
    MP = MyPlot(path,file,token,PlotFlag)
    MP.ReadTestData(legend)
    MP.ConnectDropbox()
    MP.PushFileDropbox('/LCWA/ROTW/')
