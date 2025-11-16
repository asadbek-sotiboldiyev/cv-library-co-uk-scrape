import pandas as pd
from pagination import get_pagination_numbers, go_to_next_page
from dataextraction import get_job_details
from searcher import search_keyword
from selenium.webdriver.common.keys import Keys
    
def scrape_jobs(driver, searchkeywords: list, tools_list: list) -> pd.DataFrame:
    all_data = []

    for keyword in searchkeywords:
        search_keyword(driver, keyword)
        print(f"*** Searching for jobs with keyword: {keyword}")
    
        page_numbers = get_pagination_numbers(driver)
        if not page_numbers:
            page_numbers = [1]
        for idx, _ in enumerate(page_numbers):
  
            title, date, logo, company, salary, jobid, location, skills = get_job_details(driver, tools_list)
            keyword_column = [keyword] * len(title)
            source = ['cv-library.co.uk']* len(title)
            country = ['UK']* len(title)
            
            all_data.extend(zip(date,keyword_column, title, company, logo, country, location, skills, salary, source, jobid))
            
            if idx < len(page_numbers) - 1:
                go_to_next_page(driver)
    
    columns = [ "Posted_date",  "Job Title from List", "Job Title", "Company", "Company Logo URL", "Country", "Location", "Skills", "Salary Info", 'Source', "Job ID"]
    df = pd.DataFrame(all_data, columns=columns)
    df['Skills'] = df['Skills'].apply(lambda x: ', '.join(x))
    print("===== Data saved to database")
    return df
