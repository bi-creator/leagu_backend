from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query import executeQuery
from datetime import datetime
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


@app.get('/getCourts')
def getCourts():
    data=executeQuery('select * FROM public.play_grounds where under_maintainence=false')
    return data
    
@app.get('/getAvailableSlots')
def getSlots(court_id):
    data=executeQuery(f"""select st.slot_id,st.slot_time from public.slots st 
where st.slot_id not in (select slot_id from public.booking_table where ground_id={court_id})""")
    return data

@app.get('/getBookings')
def getBookings():
    data=executeQuery('select * FROM public.booking_table where is_cancled=false ')
    return(data)

@app.post('/addBooking')
def addBooking(name, email,contact,ground_id,slot_id):
    booking_id=str(datetime.now())
    datatoinsert=(booking_id, name, email,contact,ground_id,slot_id)
    data=executeQuery("INSERT INTO booking_table (booking_id, name, email,contact,ground_id,slot_id) VALUES (%s,%s,%s,%s,%s,%s)",datatoinsert)
    return data

@app.post('/cancleBooking')
def cancleBooking(booking_id):
    data=executeQuery("UPDATE booking_table SET is_cancled = %s WHERE booking_id = %s",(True,booking_id))
    return data

    