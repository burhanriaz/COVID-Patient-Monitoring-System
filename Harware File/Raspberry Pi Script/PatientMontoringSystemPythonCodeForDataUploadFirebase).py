import serial  

#import http.client as http  
import datetime
import urllib

import pyrebase
from datetime import datetime
config  = {
    "apiKey": "AIzaSyDgfx-eqh1uxy0gJ4aMn6-RJupDQkvWSEE",
    "authDomain": "pateint-monitoring-syste-171be.firebaseapp.com",
    "databaseURL": "https://pateint-monitoring-syste-171be-default-rtdb.firebaseio.com",
    "projectId": "pateint-monitoring-syste-171be",
    "storageBucket": "pateint-monitoring-syste-171be.appspot.com",
    "messagingSenderId": "545144241140",
    "appId": "1:545144241140:web:772ef8efbcb503172a17a1",
    "measurementId": "G-SZ139N3PH3"
};
firebase = pyrebase.initialize_app(config)



#ser = serial.Serial('/dev/ttyACM0',9600)
serport = serial.Serial('/dev/ttyACM0',115200)



def find(val):
    Str=val

    if (Str.find("*")!=-1):
        for w in Str.split():
            if w.isdigit():
                BPM=int(w)
                B=1
                return BPM,B
        #B=1
       # print(B,Str)
    elif (Str.find("$")!=-1):
        
        for w in Str.split():
            if w.isdigit():
                SPO2=int(w)
                B=2
                return SPO2,B
      #  B=2
        #print(B,Str)
                  

      
def upload_to_firebase(BPM,SPO2):
    db = firebase.database()
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    bedNo=3
    bpm=BPM
    spo2=SPO2

    data = {
        
        "DateTime":dt_string,
        "BPM":bpm,
        "SPO2":spo2,
        "Bed No":bedNo
       }
     #db.child("Patient").child(cnic).set(data) #use set  function if we have uniqe key like cnic
    db.child("Sensor").child(bedNo).child(dt_string).set(data)
    

while True:
    try:  

       # read_serial=serport.readline()
        #Str= read_serial.decode('utf-8').strip()
        
       #print(Str)
        BPM=-1
        SPO2=-1
        B=-1
    
        
        while (BPM==-1 or SPO2==-1):
            read_serial=serport.readline()
            Str= read_serial.decode('utf-8').strip()
            if ((Str.find("*")!=-1) or (Str.find("$")!=-1)):
                temp,B= find(Str)
                if (B==1):
                    BPM=temp
                elif(B==2):
                    SPO2=temp
##            else:
##                B=0
            
        '''BPM=-1
        SPO2=-1
        if (B==1 or B ==2):
            for w in Str.split():
                if w.isdigit() and B==1:
                  BPM=int(w)
                elif w.isdigit() and B==2:
                 SPO2=int(w)'''

        if (BPM>-1 or SPO2>-1):
            print("\nBPM & SPO2",BPM,SPO2)
                #print(BPM)
           # print("\nSPO2",SPO2)
                #print(SPO2)
            upload_to_firebase(BPM,SPO2)
           
##        else:
##            upload_to_ts(B,B)
        
        
        #print (bpm)
        #print(spo2)

          

    except KeyboardInterrupt:  

        print ("\nExiting.....")  

        break  
