import pandas as pd
import pyodbc
from scraper import scrape_jobs
from savetodatabase import savetodb, create_connection
from aititlefilter import filtercolumns

def add_posted_date(job_data: pd.DataFrame, searchkeywords: list) -> pd.DataFrame:
    job_data['Posted_date'] = pd.to_datetime(job_data['Posted_date'], errors='coerce')
    job_data = job_data.dropna(subset=['Posted_date'])
    job_data['Posted_date'] = job_data['Posted_date'].dt.strftime('%m/%d/%Y %I:%M')
    job_data = filtercolumns(job_data, searchkeywords)
    job_data.index = pd.RangeIndex(start=1, stop=len(job_data)+1, step=1)
    job_data.index.name = "ID"
    return job_data

def save_all_in_one(driver, searchkeywords: list, tools_list: list, log_file_name: str):
    '''
    Get all datas then save
    '''
    # job_data = scrape_jobs(driver, searchkeywords, tools_list)
    job_data = scrape_jobs(driver, searchkeywords, tools_list)

    driver.quit()

    job_data = add_posted_date(job_data, searchkeywords)
    conn = create_connection()
    if conn is None:
        print("==== Database connection fail")
        return
    savetodb(job_data, conn)
    job_data.to_excel(log_file_name + "_jobs.xlsx")
    print("*** All data saved to database")
    conn.close()

