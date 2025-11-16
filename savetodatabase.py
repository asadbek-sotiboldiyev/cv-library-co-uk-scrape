import pyodbc

def create_connection():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=localhost\\SQLEXPRESS;"
            "Database=maab_task;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print(f'==== Error creating connection: {e}')
        return

def savetodb(job_data, conn):
    try:
        cursor = conn.cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'CVlibraryJobs')
        BEGIN
            CREATE TABLE CVlibraryJobs (
                ID INT,
                Posted_date NVARCHAR(100),
                Job_Title_from_List NVARCHAR(255),
                Job_Title NVARCHAR(255),
                Company NVARCHAR(255),
                Company_Logo_URL NVARCHAR(MAX),
                Country NVARCHAR(50),
                Location NVARCHAR(255),
                Skills NVARCHAR(MAX),
                Salary_Info NVARCHAR(255),
                Source NVARCHAR(255)
            )
        END
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert data into the table
        insert_query = """
        INSERT INTO CVlibraryJobs (ID, Posted_date, Job_Title_from_List, Job_Title, Company, Company_Logo_URL, Country, Location, Skills, Salary_Info, Source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        for idx, job in job_data.iterrows():
            try:
                cursor.execute(insert_query, 
                               idx,
                               job['Posted_date'], 
                               job['Job Title from List'], 
                               job['Job Title'], 
                               job['Company'], 
                               job['Company Logo URL'], 
                               job['Country'], 
                               job['Location'], 
                               job['Skills'], 
                               job['Salary Info'], 
                               job['Source'])
            except Exception as row_error:
                print(f"==== Failed to insert row {idx}: {row_error}")

        conn.commit()
        print("===== Data saved to SQL Server")

    except Exception as e:
        print(f"==== Failed to save data to SQL Server: {e}")

    finally:
        cursor.close()
        # conn.close()
