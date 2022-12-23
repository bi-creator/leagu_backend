from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query import executeQuery
from datetime import datetime,timedelta
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.post('/addCourts')
def addCourts(undermaintainence:bool,court_name):
    court_id=str(datetime.now())
    data=executeQuery(f"INSERT INTO play_grounds ('ground_id','ground_name','under_maintainence') VALUES ('{court_id}','{court_name}','{undermaintainence}')")
    return data

@app.post('/addSlots')
def addSlots(slot_time):
    slot_id=str(datetime.now())
    data=executeQuery(f"INSERT INTO slots ('slot_id','slot_time') VALUES ('{slot_id}','{slot_time}')")
    return data


@app.get('/getCourts')
def getCourts():
    data=executeQuery('select * FROM play_grounds ')
    return data
    
@app.get('/getAvailableSlots')
def getSlots(court_id):
    print(court_id)
    data=executeQuery(f"select st.slot_id,st.slot_time from slots st where (st.slot_id not in (select slot_id from booking_table bt where bt.ground_id='{court_id}' and substr(bt.booking_id, 1, 10)= '{str(datetime.now())[0:10]}' and bt.is_cancled=false)) or (st.slot_id in (select slot_id from booking_table bt where bt.ground_id='{court_id}' and substr(bt.booking_id, 1, 10)='{str(datetime.now())[0:10]}' and bt.is_cancled=true))")
    return data

@app.get('/getBookings')
def getBookings():
    data=executeQuery(f"""select bt.booking_id,bt.name,bt.email,bt.contact,pg.ground_name,sl.slot_time FROM booking_table bt
join play_grounds pg ON pg.ground_id = bt.ground_id
join slots sl ON sl.slot_id = bt.slot_id
where is_cancled=false and substr(bt.booking_id, 1, 10)= '{str(datetime.now())[0:10]}'""")
    return(data)

@app.post('/addBooking')
def addBooking(name, email,contact,ground_id,slot_id):
    booking_id=str(datetime.now())
    data=executeQuery(f"INSERT INTO booking_table (booking_id, name, email,contact,ground_id,slot_id) VALUES ('{booking_id}','{name}','{email}','{contact}','{ground_id}','{slot_id}')")
    return data

@app.put('/cancleBooking')
def cancleBooking(booking_id):
    data=executeQuery(f"UPDATE booking_table SET is_cancled = true WHERE booking_id = '{booking_id}'")
    return data

@app.delete('/deletebookings')
def deletebookings():
    data=executeQuery(f"DELETE FROM booking_table WHERE booking_id<'{str(datetime.now()-timedelta(days=2))}';")
    return data  


@app.put('/updatedcouty')
def updatedcouty(court_maintainence:bool,court_id):
    data=executeQuery(f"UPDATE play_grounds SET under_maintainence = '{court_maintainence}' WHERE ground_id = '{court_id}'")
    return data