from re import L
from textwrap import indent
from typing import List, Optional, Any
from pydantic import BaseModel
from pydantic.utils import GetterDict


class uofield(BaseModel):
    data : list[str] = None
    #fieldname : str = ""


class dataconstants():
    AM = str(chr(254))
    VM = str(chr(253))
    SVM = str(chr(252))    
    



class mrecord(BaseModel):
    record : list[uofield] = None
    
    def addrec(self, Data=""):
        """Add a attribute to mRecord object i.e. Attribute in Dynamic array"""
        rec = uofield(data=[Data])
        if self==None:
            self = mrecord(record=[rec])
        else:
            if self.record==None:
                self.record = [rec]
            else:
                self.record.append(rec)
                        
        return self


    def __getitem__(self, item):
        return  self.record[item]   


    def __setitem__(self, item, value):
        if type(item) == int:
            self.__setitem__((item,0), value)
            """if self.record==None:
              rec = [uofield(data=[""])]
              self.record = rec
            self.record[item] = uofield(data=[value])"""
        else:
            if len(item) == 2:
                subpos = item[1]
                item   = item[0]
                if self == None:
                    self = mrecord(record=[uofield(data=[])])
                if self.record == None:
                    self.record =  [uofield(data=[])]                  
                if len(self.record) <= item+1:
                    for i in range(len(self.record),item+1):
                        self.record.append(uofield(data=[""]))
                if self.record[item].data == None:
                    self.record[item].data = uofield(data=[""])
                if len(self.record[item].data)+1 < subpos:
                    rnpos = subpos - (len(self.record[item].data)+1)
                    for k in range(rnpos):
                        self.record[item].data.insert(len(self.record[item].data),"")        
                self.record[item].data.insert(subpos,value)


    def getString(self):
        """Converts a mRecord Array to Dynamic Array String"""
        stringval = ""
        for xcntr in range(len(self.record)): #var in self.record:
            vmstr = ""            
            var = self.record[xcntr]
            for vcntr in range(len(var.data)):
                 #fld in var.data:
                fld = var.data[vcntr]
                
                if vcntr+1 == len(var.data):
                    vmstr += fld 
                else:
                    vmstr += fld + dataconstants.VM
                        
            if xcntr+1 == len(self.record):
                stringval += vmstr
            else:
                stringval += vmstr + dataconstants.AM
        return stringval
    

    def populateArray(self, vmString):
        """Converts a Dynamic array passed in vmString to mRecord Object"""
        #print(" populateArray ....converting ...",vmString)
        vmArr = vmString.split(dataconstants.AM)
        self = mrecord(record=[uofield()])  #record = [uofield(data=[])])
        for xcntr in range(len(vmArr)): #var in self.record:
            attr = vmArr[xcntr]
            vmAttr = attr.split(dataconstants.VM)
            vmfld = uofield(data=vmAttr)
            if xcntr==0:
                self.record = [vmfld]
            else:
                self.record.append(vmfld)
            
        return self


class multi_svr_object(BaseModel):
    ProcessName : str
    ProcessParams : mrecord

