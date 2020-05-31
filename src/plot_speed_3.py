#!/usr/bin/env python

'''
Created on Jan 23, 2020

@author: klein
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

def MyPythonVersion():
    if (sys.version_info[0] == 3):
        print(' we have python 3')
        vers = True
    else:
            
        vers = False
    return vers
    

def MyTime(b):
    s=b.decode('ascii')
    #print(s)
    a =md.date2num(datetime.datetime.strptime(s,'%H:%M:%S'))  
      
    return a
def MyDate(bb):
    s=bb.decode('ascii')
    #print(s)
    aa =md.date2num(datetime.datetime.strptime(s,'%d/%m/%Y'))    
    return aa


drop = False
#for k in range(len(sys.argv)):
#    print sys.argv

if len(sys.argv)==2:
    # check if file exists
    try:
        os.path.isfile((sys.argv[1]))
        filename = sys.argv[1]
        file1=filename
    except:
        print('no file')
        sys.exit(0)
elif len(sys.argv)==3:
    drop=True
    

else:
    print( ' to run the program you have to give a filename \n plot_speed.py inputfile ')
    print(' You have to give the token file')
    sys.exit(0)
    
# connect to dropbox
if(drop):
    f=open(sys.argv[2],"r")
    data =f.readline() #key for encryption
    data=data.strip('\n')

#connect to dropbox
    dbx=dropbox.Dropbox(data)
    myaccount = dbx.users_get_current_account()
    print('***************************dropbox************************************')
    print('*                                                                    *')
    print( 'first = ',myaccount.name.given_name,'last = ',myaccount.name.surname  )
    print( 'email account = ',myaccount.email)
    print('*                                                                    *')
    print('***************************dropbox************************************')

# get dropbox file

    file = '/LCWA/'+ sys.argv[1]
    
    dir = os.path.expanduser("~")
    print(len(sys.argv[1]))
          
    if (len(sys.argv[1])> 28):
        
        temp = sys.argv[1][5:]
    
    else:
        
        temp =  sys.argv[1]
    file1 = dir+'/scratch/'+temp
    print(file,'  ',file1)
    filename = dbx.files_download_to_file(file1,file)
    #filename = dbx.files_download_to_file('/Users/klein/scratch/LC04_2020-04-20speedfile.csv','/LCWA/LC04/LC04_2020-04-20speedfile.csv')
    
    #print filename         
x1 = []
y1 = []
x2 = []
y2 =[]

# check for data integrtity by writing file to temporary buffer

temp_file = open('temp.txt',"w")
counter = 0
for line in open(file1, 'r'):

    a = line.split(',')
    if(len(a)< 9):
        print ('problem',a)
        print ('ignore data point at line ',counter+1)
    else:
        temp_file.write(line)
    counter = counter + 1
#file1.close()
temp_file.close()
   

if(MyPythonVersion):
    with open('temp.txt') as f:
        for i, l in enumerate(f):
            pass
        lines=i   # used for arrays

    dtype=np.dtype(np.float64)
    x0 =np.zeros(lines)
    y1=np.zeros(lines)
    y2=np.zeros(lines)
    format1 = "%d/%m/%Y %H:%M:%S"
    
    

    with open('temp.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        k=0
        for row in spamreader:
            #print(', '.join(row))
            #print(row[0],row[7])  
            
            if(k>0):
                date_str = row[0]+' '+row[1]

                aa =md.date2num(datetime.datetime.strptime(date_str,format1))
                x0[k-1] = aa
                y1[k-1] = row[7]
                y2[k-1] = row[8]
                #print(x0[k-1] , '  ',y1[k-1])

            #print(aa)
            k=k+1
            
            
    
#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"        
#    x0,x1,y1,y2 = np.loadtxt('temp.txt', delimiter=',',
#                  unpack=True,usecols=(0,1,7,8),
#        converters={ 0:MyDate, 1: MyTime},skiprows =1)
#    print(x0[1],x1[1])


#filename = "/Users/klein/speedfiles/2020-02-09speedfile.csv"  
else:      
    x1,y1,y2 = np.loadtxt('temp.txt', delimiter=',',
                   unpack=True,usecols=(1,7,8),
#        converters={ 1: md.strpdate2num('%d/%m/%Y-%H:%M:%S')})
        converters={ 1: md.strpdate2num('%H:%M:%S')},skiprows=1)
        #converters={0:bytespdate2num('%H:%M:%S')},skiprows=1)
        #converters={ 1: MyTime},skiprows =1)


np.set_printoptions(precision=2)
fig=plt.figure() 
ax=fig.add_subplot(1,1,1)
#ax.text(.1,.36,'Average $\mu$ and Standard deviation $\sigma$',weight='bold',transform=ax.transAxes,fontsize=13)
#ax.text(.1,.23,r'$\mu_{up}     = $'+str(np.around(np.mean(y2),2))+' '+'[Mb/s]'+r'   $\sigma_{up} =     $'+str(np.around(np.std(y2),2)),transform=ax.transAxes,fontsize=12)
#ax.text(.1,.3,r'$\mu_{down} = $'+str(np.around(np.mean(y1),2))+' '+'[Mb/s]'+r'   $\sigma_{down} = $'+str(np.around(np.std(y1),2)),transform=ax.transAxes,fontsize=12)

plt.plot_date(x0,y1,'bs',label='\n blue DOWN ',markersize =2)
plt.plot_date(x0,y2,'g^',label=' green UP',markersize =2)
#plt.text(1.,1.,r' $\sigma = .1$')
plt.grid(True)
print(x0)
ax.xaxis.set_major_locator(md.MinuteLocator(interval=1440))
ax.xaxis.set_major_formatter(md.DateFormatter('%d/%m/%y %H:%M'))
plt.xlabel('Time')
plt.ylabel('Speed in Mbs')
if(drop):
    plt.title('Speedtest LCWA using '+file)
else:
    plt.title('Speedtest LCWA using '+file1)
    
plt.legend(facecolor='ivory',loc="lower right",shadow=True, fancybox=True)

if(np.around(np.mean(y1),2) > 21.):
    plt.ylim(0.,41.) # set yaxis limit
elif(np.around(np.mean(y1),2) <= 21. and np.around(np.mean(y1),2) > 12.):
    plt.ylim(0.,24.) # set yaxis limit
elif(np.around(np.mean(y1),2) <= 12. and np.around(np.mean(y1),2) > 7.):
    plt.ylim(0.,12.) # set yaxis limit
             # set yaxis limit
elif(np.around(np.mean(y1),2) <= 7. ):
    plt.ylim(0.,7.) # set yaxis limit
print('mean  ' ,np.around(np.mean(y1),2) )
print('std  ' ,np.around(np.std(y1),2) )

 # set yaxis limit
plt.xticks(rotation='vertical')
plt.tight_layout()
file2 = file1.replace('csv','pdf')

print (file2)
fig.savefig(file2, bbox_inches='tight')
plt.show()


if __name__ == '__main__':
    pass