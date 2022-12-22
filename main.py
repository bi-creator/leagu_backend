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
    print(court_id)
    data=executeQuery(f"select st.slot_id,st.slot_time from public.slots st where st.slot_id not in (select slot_id from public.booking_table bt where bt.ground_id='{court_id}' and TO_DATE(bt.booking_id,'YYYY-MM-DD HH24:MI:SS')=CAST( NOW() AS Date) )")
    return data

@app.get('/getBookings')
def getBookings():
    data=executeQuery("""select bt.name,bt.email,bt.contact,pg.ground_name,sl.slot_time FROM public.booking_table bt
join public.play_grounds pg ON pg.ground_id = bt.ground_id
join public.slots sl ON sl.slot_id = bt.slot_id
where is_cancled=false and TO_DATE(booking_id,'YYYY-MM-DD HH24:MI:SS')=CAST( NOW() AS Date)""")
    return(data)

@app.post('/addBooking')
def addBooking(name, email,contact,ground_id,slot_id):
    booking_id=str(datetime.now())
    datatoinsert=(booking_id, name, email,contact,ground_id,slot_id)
    data=executeQuery("INSERT INTO booking_table (booking_id, name, email,contact,ground_id,slot_id) VALUES (%s,%s,%s,%s,%s,%s)",datatoinsert)
    return data

@app.put('/cancleBooking')
def cancleBooking(booking_id):
    data=executeQuery("UPDATE booking_table SET is_cancled = %s WHERE booking_id = %s",(True,booking_id))
    return data

@app.delete('/deletebookings')
def deletebookings():
    data=executeQuery("DELETE FROM public.booking_table WHERE TO_DATE(booking_id,'YYYY-MM-DD HH24:MI:SS')<(CAST( NOW() AS Date)-2);")
    return data  


@app.put('/updatedcouty')
def updatedcouty(court_maintainence:bool,court_id):
    data=executeQuery("UPDATE public.play_grounds SET under_maintainence = %s WHERE ground_id = %s",(court_maintainence,court_id))
    return data