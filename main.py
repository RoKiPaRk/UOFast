# Main Launch program within UOFast to initialize connections and start FASTApi server.
# (c) UOFast
#
#


from ast import Str
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from gsocketpool import Pool
from UOFastDataArray import * 
import json
import uopy
import UOFastConfig
from gsocketpool.connection import m_connection
from fastapi.openapi.utils import get_openapi

#load UOFast.cfg params
configparams = UOFastConfig.uofastconfiguration()

app = FastAPI()
#pool = None
    
options = dict(user=configparams.UOuser, pw=configparams.UOpassword)

#this is where the magic happens
pool = Pool(m_connection, options, initial_connections=configparams.initial_connections, 
            max_connections=configparams.max_connections, 
            reap_interval=configparams.reap_interval)


@app.on_event("shutdown")
def shutdown_event():
    """very important for a clean shutdown and clear Pool sessions"""
    for conn in pool._pool: 
        conn.close()
            
@app.get('/UOFast')
def uofast_process(multi_svr_object : multi_svr_object):
    print("multi_svr_object",multi_svr_object)

    try:
        print("Params",multi_svr_object.ProcessParams)
        #multi_svr_object.ProcessParams = json.loads(multi_svr_object.ProcessParams)
        UOFast = _callsubroutine(multi_svr_object.ProcessName, multi_svr_object.ProcessParams.getString())
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e))
        #FastMVApi = None

    return {'UOFast': UOFast}

@app.post('/UOFast')
def uofast_process(multi_svr_object : multi_svr_object):
    print("multi_svr_object",multi_svr_object)

    try:
        print("Params",multi_svr_object.ProcessParams)
        #multi_svr_object.ProcessParams = json.loads(multi_svr_object.ProcessParams)
        UOFast = _callsubroutine(multi_svr_object.ProcessName, multi_svr_object.ProcessParams.getString())
    except Exception as e:
        raise HTTPException(status_code=418, detail=str(e.detail))
        #FastMVApi = None

    return {'UOFast': UOFast}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="UOFast API",
        version="1.1.0",
        description="Restful connection pooling service for U2 databases, built on Python, FastAPI, uopy \n ( uopy, U2 database are registered trademarks of Rocket software. )", 
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

def _callsubroutine(Processname, Processparams):
    retVars=""
    mstring = ""
    print("Call subroutine",Processname,Processparams)
    try:
        with pool.connection() as conn:
            subcount=0
            errVars=""
            sub = uopy.Subroutine(Processname, 3, session=conn.socket)
            conn.logger_info("params" + Processparams)
            sub.args[0] = Processparams
            sub.args[1] = retVars
            sub.args[2] = errVars
            conn.logger_info("BEGIN Calling Subroutine ..." + Processname)
            conn.logger_info("Params=" + str(Processparams))
            sub.call()
            retVars = str(sub.args[1]) #OUTVALS
            errVars = sub.args[2]  #ERRVALS
            print("errors returned ", str(errVars))            
            if str(errVars) != "":
                if str(errVars[0]) != "":
                    errVars = str(errVars).replace(dataconstants.VM, "")
                    raise HTTPException(status_code=418, detail=str(errVars))
                    #raise Exception(str(errVars[0]))
            conn.logger_info("END Calling Subroutine ..." + Processname)
            #Now parse the return object            
            mstring = mrecord()
            mstring = mstring.populateArray(retVars)

    except Exception as e:
        retVars = ""
        print("Error calling sub ", str(e))
        raise HTTPException(status_code=418, detail=str(e.detail))   
    
    return mstring