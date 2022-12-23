import sqlite3
conn = sqlite3.connect('leadgu')
conn.execute("""CREATE TABLE IF NOT EXISTS play_grounds
(
    "ground_id" character varying  NOT NULL,
    "ground_name" character varying NOT NULL,
    "under_maintainence" boolean NOT NULL,
    CONSTRAINT play_grounds_pkey PRIMARY KEY ("ground_id")
) """)
conn.execute("""CREATE TABLE IF NOT EXISTS slots
(
    "slot_id" character varying NOT NULL,
    "slot_time" character varying NOT NULL,
    CONSTRAINT slots_pkey PRIMARY KEY ("slot_id")
)""")
conn.execute("""CREATE TABLE IF NOT EXISTS booking_table
(
    "booking_id" character varying  NOT NULL,
    "name" character varying  NOT NULL,
    "email" character varying  NOT NULL,
    "contact" character varying  NOT NULL,
    "ground_id" character varying  NOT NULL,
    "slot_id" character varying  NOT NULL,
    "is_cancled" boolean NOT NULL DEFAULT false,
    CONSTRAINT booking_table_pkey PRIMARY KEY ("booking_id"),
    CONSTRAINT "ground_id" FOREIGN KEY ("ground_id")
        REFERENCES play_grounds ("ground_id") MATCH SIMPLE
       
    CONSTRAINT slot_id FOREIGN KEY ("slot_id")
        REFERENCES slots ("slot_id") MATCH SIMPLE
        
)""")
conn.close()