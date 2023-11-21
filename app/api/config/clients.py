#!/usr/bin/python

#%%
from modules import *

######################
####    AWS S3    ####
######################

#%%
def s3_connect():
    try:
        s3_client = boto3.client('s3')
        print("S3 Client Connected")
    except Exception as e:
        print(f"S3 Client Connection Error: {e}")
        s3_client = None
    return s3_client

##########################
####    PostgreSQL    ####
##########################

# Connect to PostgreSQL
# Run Postgres Locally
# brew services start postgresql

#%%
# Global variable for connection pool
connection_pool = None

def initialize_connection_pool():
    global connection_pool
    try:
        # Get database connection details from environment variables
        db_host = os.environ.get('POSTGRES_DB_HOST', 'localhost')
        db_port = os.environ.get('POSTGRES_DB_PORT', '5432')
        db_name = os.environ.get('POSTGRES_DB_NAME')
        db_user = os.environ.get('POSTGRES_DB_USER')
        db_password = os.environ.get('POSTGRES_DB_PASSWORD')

        # Initialize the connection pool => auto scale threads when needed
        connection_pool = psycopg2.pool.ThreadedConnectionPool(1, 10,
                                                            host=db_host,
                                                            port=db_port,
                                                            dbname=db_name,
                                                            user=db_user,
                                                            password=db_password)
    except psycopg2.Error as e:
        print(f"Error initializing connection pool: {e}")

def get_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        print("Connection pool is not initialized.")
        return None

def release_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)

def connect_to_postgres():
    try:
        # Get a connection from the pool
        conn = get_connection()
        if conn:
            # Do something with the connection
            print(f"Connected to PostgreSQL: {conn.status}")
            # Release the connection back to the pool
            release_connection(conn)
        else:
            print("Failed to obtain a connection.")
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

# Initialize the connection pool
initialize_connection_pool()

# Example usage
connect_to_postgres()


def create_table():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='your_database_name',
            user='your_username',
            password='your_password'
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Define the SQL query to create the table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS your_table_name (
            column1 datatype1,
            column2 datatype2,
            ...
        )
        '''

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print("Table created successfully!")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

# %%
