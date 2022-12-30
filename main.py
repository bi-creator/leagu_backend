from fastapi import FastAPI,Response, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from query import executeQuery
from datetime import datetime,timedelta
import pytz
from pydantic import BaseModel
class BookCourt(BaseModel):
    name: str
    email:str
    contact:str
    ground_id:str
    slot_id:str
class addCourt(BaseModel):
    court_name: str
    undermaintainence:bool
class booking_id(BaseModel):
    booking_id:str
class numberofdates(BaseModel):
    numberofdays:str
name='NAME'
password="PASSWORD"
IST = pytz.timezone('Asia/Kolkata')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.post('/addCourts')
def addCourts(courtdata:addCourt):
    court_id=str(datetime.now(IST))
    data=executeQuery(f"INSERT INTO play_grounds ('ground_id','ground_name','under_maintainence') VALUES ('{court_id}','{courtdata.court_name}','{courtdata.undermaintainence}')")
    return data

@app.post('/addSlots')
def addSlots(slot_time):
    slot_id=str(datetime.now(IST))
    data=executeQuery(f"INSERT INTO slots ('slot_id','slot_time') VALUES ('{slot_id}','{slot_time}')")
    return data


@app.get('/getCourts')
def getCourts():
    data=executeQuery('select * FROM play_grounds ')
    return data
    
@app.get('/getAvailableSlots')
def getSlots(court_id):
    print(court_id)
    data=executeQuery(f"select st.slot_id,st.slot_time from slots st where st.slot_id not in (select slot_id from booking_table bt where bt.ground_id='{court_id}' and substr(bt.booking_id, 1, 10)= '{str(datetime.now(IST))[0:10]}' and bt.is_cancled=0) and cast(substr(st.slot_time,1,2) AS INTEGER )>{int(datetime.now(IST).hour)} ")
    return data

@app.get('/getBookings')
def getBookings():
    data=executeQuery(f"""select bt.is_cancled, bt.booking_id,bt.name,bt.email,bt.contact,pg.ground_name,sl.slot_time FROM booking_table bt
join play_grounds pg ON pg.ground_id = bt.ground_id
join slots sl ON sl.slot_id = bt.slot_id
where is_cancled=0 and substr(bt.booking_id, 1, 10)= '{str(datetime.now(IST))[0:10]}'""")
    return(data)

@app.get('/getAllBookings')
def getAllBookings():
    data=executeQuery(f"""select bt.is_cancled, bt.booking_id,bt.name,bt.email,bt.contact,pg.ground_name,sl.slot_time FROM booking_table bt
join play_grounds pg ON pg.ground_id = bt.ground_id
join slots sl ON sl.slot_id = bt.slot_id""")
    return(data)

@app.post('/addBooking')
def addBooking(bookongdetails:BookCourt):
    booking_id=str(datetime.now(IST))
    data=executeQuery(f"INSERT INTO booking_table (booking_id, name, email,contact,ground_id,slot_id,is_cancled) VALUES ('{booking_id}','{bookongdetails.name}','{bookongdetails.email}','{bookongdetails.contact}','{bookongdetails.ground_id}','{bookongdetails.slot_id}',{0})")
    return data

@app.put('/cancleBooking')
def cancleBooking(booking_id:booking_id):
    data=executeQuery(f"UPDATE booking_table SET is_cancled =1 WHERE booking_id = '{booking_id.booking_id}'")
    return data

@app.post('/deletebookings')
def deletebookings(days:numberofdates):
    data=executeQuery(f"DELETE FROM booking_table WHERE booking_id<'{str(datetime.now(IST)-timedelta(days=int(days.numberofdays)))}';")
    return data  


@app.put('/updatedcouty')
def updatedcouty(court_maintainence:bool,court_id):
    data=executeQuery(f"UPDATE play_grounds SET under_maintainence = '{court_maintainence}' WHERE ground_id = '{court_id}'")
    return data

@app.get('/login',status_code=200)
def login(username,userpass,response: Response):
    if(username!=name):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    elif(userpass!=password):
        response.status_code=status.HTTP_401_UNAUTHORIZED
        return
    else:
        response.status_code=status.HTTP_200_OK
        return {'accessToken':"fakeToken",'error':[]}
