# Installation

UOFast is a U2 UOPY based restful service which pools U2 UOPY connections and accepts GET/PUT type requests to U2 databases. Its based on FastAPI, gsocketpool, pydantic and uopy. This is an opensource sample, to demonstrate the capabilities of UOPY connectivity using a restful service. #U2 #uopy #sample #python #Unidata #example.

Check Python installation - Since uofast is based on python, it need python version 3.9.1 and above to function.

1. **How to check python version ?**

\> _Python -V_

If the version installed on the machine is > 3.9.1, then skip to step 3.
	Tip : If you have an Older version of Python already installed, please remove that from the PATH in your environment and leave the new one in.

2. **How to install python?**

Please download python 3.9.1 from the below site.

[https://www.python.org/downloads/release/python-391/](https://www.python.org/downloads/release/python-391/%20%20)

3. **Install required packages**

The below step will install all the required "include" packages for uofast.

\>_pip install -r requirements.txt_

# Setup

_UOFast.cfg_ **- Edit required configuration settings for uofast.**

Edit uofast.cfg in the uofast installation directory. Some of the setting have been marked with \<Do not change\> - which means these are recommended and tested, so there is no need to change.

	[UOConnectionSettings]

	UOhost = <Server name or IP Address\>
	UOaccount = <Account path e.g. C:\U2\UD82\DEMO\>
	UOservice = <udcs for Unidata\>
	UOport = <UniRPC port in UniObjects e.g. 31438\>
	UOuser = <Unidata user id \>
	UOpassword = <Unidata password\>

	[ApplicationSettings]

	Mainlogname=UOFastMainAPI.log <Main application Log file name\>
	UOConnectionLogs=UOConnectionProcesses.log <Log file pertinent to each UOPY connection\>

	[PoolSettings]
	Initial\_connections : 2 <Number of minimum connection to establish in Uniobjects/uopy\>
	max\_connections : 2 <Number of MAX connection to establish in Uniobjects/uopy\>
	session\_timeout : 600 <Do not change\>
	reap\_interval : 180 <Do not change\>

# Runtime

Startup of UOFast in included in a .bat file – uofaststart.bat. The primary command used to startup UOFast is :

_python -m uvicorn main:app --port 8200_

Tip : The port number can be manipulated, to select a port of your choice.

After invoking \>uofaststart.bat, the output should look similar to below :

![](RackMultipart20220926-1-gwyz19_html_2e7a7741c26f7e62.png)

Tip : Please check uofastlogs directory to check for UOPY connection status. If you are not able to connect to the target U2 database, there might be some configuration issues in uofast.cfg.

# Usage

###

### Testing UOFast service

As per the above screenshot example, your UOFast service has been invoked at [http://127.0.0.1:8200](http://127.0.0.1:8200/). Since UOFast uses FastAPI, it has an in-built "Swagger" interface for testing purposes. 
You can invoke the swagger documentation of the API by invoking the Url [http://127.0.0.1:8200/docs](http://127.0.0.1:8200/docs) for your UOFast installation.

![](RackMultipart20220926-1-gwyz19_html_32d3c41a504cd18d.png)

### Sample requests

Requests to UOFast, can be made using any platform supporting restful requests e.g. .NET, Java or Python.

The below example is based on python "requests" model. The assumption is that,

1. a basic program is compiled & cataloged in the DEMO account of U2 Unidata.
2. The UOFast connections point to the sample Unidata DEMO account

A Sample program has been included in the UOFast install directory – (Example = TEST.SUB)

Tip – The standard UOFast API uses 3 parameters within BASIC programs to pass data to the U2 database and return as output. Ie. SUBROUTINE SUBNAME(INPUTDATA, OUTPUTDATA, ERRORDATA). NOTE: Additional parameters are not supported.

A Tkinter based GUI program has been included in the root directory to invoke the above program. This will give you an example to invoke restful services and consume them in GUI/Web programs. (Example = uofast\_tk\_sample.py)

Additional Tip : A Successful connection will return 200, the standard OK status code. An error will return 418, with the error returned from the basic program.

Examples :

#### BASIC CODE : (Should be compiled and cataloged on the server, in the install account)

	SUBROUTINE TEST.SUB(INPUTDATA, OUTPUTDATA, ERRORDATA)

	\* Sample subroutine to get information from INPUTDATA and send output
	\* using OUTPUTDATA using **UOFast**
	\*
	\*****************************************************************************

	OUTPUTDATA = ""; ERRORDATA = ""
	OPEN 'CUSTOMER' TO CUSTOMER ELSE ERRORDATA = "NO CUSTOMER OPEN";RETURN
	CUST.ID = INPUTDATA\<1\>
	READ CUST.REC FROM CUSTOMER, CUST.ID ELSE ERRORDATA\<1\> = CUST.ID:" NOT FOUND..."
	OUTPUTDATA = CUST.REC
	RETURN

####

#### PYTHON CODE (to invoke the above program)
	
	rec = UOFastDataArray.mrecord()
	rec[0] = "10"
	
	#Create the request Object
	mObject = UOFastDataArray.multi_svr_object(ProcessName="TEST.SUB", ProcessParams=rec)
	
	#Post the Request object to UOFast URL
	x = requests.post(api_url, data = mObject.json(indent=2))
	
	if x.status_code != 200:
		rettext = "**error returned = ",x.status_code, json.loads(x.text).get("detail")
	else:
		#200 is successful response
		uo_obj = json.loads(x.text)
		print(str(uo_obj))
