import os
import psycopg_pool
import csv
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = ('postgresql://FormerStudents_owner:ipVOhGX3BDu1@ep-rapid-bar-a5hqehwf-pooler.us-east-2.aws.neon.tech/FormerStudents?sslmode=require')

# Create a connection pool
connection_pool = psycopg_pool.ConnectionPool(connection_string)

# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")

# Get a connection from the pool
conn = connection_pool.getconn()

# Create a cursor object
cur = conn.cursor()
with open('Alumni.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        cur.execute("INSERT INTO alumni (firstname,lastname,gradyear,school,city,major) VALUES (%s,%s,%s,%s,%s,%s)",(row[0],row[1],row[5],row[3],row[2],row[4]))
        print(row)
conn.commit()
# Execute SQL commands to retrieve the current time and version from PostgreSQL




# Close the cursor and return the connection to the pool
cur.close()
connection_pool.putconn(conn)

# Close all connections in the pool
connection_pool.close()

# Print the results
print('Done!')