# UOFast sample program to retreive data from a subroutine call to "TEST.SUB" (source in UOFast root dir)
# I have made it very generic, and can be used as an example to derive data 
#
from ctypes import alignment
import tkinter as tk
from turtle import left
import requests
import json
import UOFastDataArray

# Top level window


frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('1000x400')

# Add the API URL
api_url = 'http://127.0.0.1:8000/UOFast'


def simulate_call():
    txtVal = inputtxt.get(1.0,"end-1c")
    jsontext = uofast_call(txtVal)
    lbl.config(text = jsontext)
    lbl.pack()

def uofast_call(custid):
    rec =  UOFastDataArray.mrecord()
    # Tip : If you are testing a program which takes more than 1 attribute of data, then add additional attributes
    #       e.g. rec[1] = 'some data'
    rec[0] = custid

    #Create the request Object
    mObject = UOFastDataArray.multi_svr_object(ProcessName="TEST.SUB", ProcessParams=rec)
    
    #Post the Request object to UOFast URL
    x = requests.post(api_url, data = mObject.json(indent=2))
    if x.status_code != 200:
        rettext = ">>error returned = ",x.status_code, json.loads(x.text).get("detail")
        #raise Exception(rettext)
    else:
        #200 is successful response
        uo_obj = json.loads(x.text)       
        
        # Get the record object from the json response  & assign to mrecord
        rec = UOFastDataArray.mrecord(record=uo_obj.get("UOFast").get('record'))
        
        i=0
        uo_str = ""
        
        #Parse through the record object

        for i in range(len(rec.record)):
            attrib = rec[i]  # Similar to DynamicArray<n>
            print("rec--", i,str(attrib))
            uo_str += (f"<{str(i)}> = {str(attrib.data)}" + '\n').format(":>100")
        rettext = uo_str

    return rettext
    
# TextBox Creation
inputtxt = tk.Text(frame,
                   height = 1,
                   width = 20)
  
inputtxt.pack()
# Button Creation
printButton = tk.Button(frame,
                        text = "Get Data", 
                        command = simulate_call)
printButton.pack()


lbl = tk.Label(frame,height=12,  wraplength=220, anchor=tk.NW, justify=tk.LEFT) #width=200,text = "", anchor='w')

lbl.pack()
  
  
# Label Creation
frame.mainloop()


