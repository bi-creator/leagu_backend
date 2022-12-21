import psycopg2
def executeQuery(query,datatoinsert=[]):
    conn = psycopg2.connect(
        database="league", user='postgres', password='manjith', host='localhost', port= '5432'
        )
    cursor = conn.cursor()
    if(datatoinsert):
        try:
            # print(query,datatoinsert)
            cursor.execute(query,datatoinsert)
            conn.commit()
            # count = cursor.rowcount
            return "Updated successfully "
        except:
            return("Something Went Wrong")
    elif('DELETE' in query):
        try:
            cursor.execute(query)
            conn.commit()
            return("Data Deleted")
        except:
            return("Something Went Wrong")

    else:
        try:
            cursor.execute(query)
            data=[]
            column_names = [desc[0] for desc in cursor.description]
            for row in cursor:
                a={}
                for col in  column_names:
                    a[col]=row[column_names.index(col)]
                data.append(a)
            conn.close()
            return(data)
        except:
            return("Something Went Wrong")
