from selenium.webdriver.common.by import By
from datetime import datetime

from scroller import scroll_to_end
from skillsextraction import getskills
from selenium.common.exceptions import NoSuchElementException

def get_job_logo(item, job_id, job_title):
    logo_element = False
    try:
        logo_element = item.find_element(By.CLASS_NAME, "job__logo")
        # logo src dan emas data-src dan olinyabdi. 
        # lazy download bo'lgani uchun, default data-src da bo'ladi, 
        # internet tezligi past bo'lsa, src ga yozilish ko'p vaqt oladi 
        logo_src = logo_element.get_attribute('data-src')
        return logo_src
    except NoSuchElementException:
        print("*** No logo available for:", job_id)
    except Exception as e:
        print("===== Error getting logo:", job_id, job_title, "======")
        print(e)
    return "No logo available"

def get_job_details(driver, tools_list):
    try:
        driver.execute_script("document.body.style.zoom='25%'")
        results_items = driver.find_elements(By.CLASS_NAME, "results__item")
        if not results_items:
            print("*** No job items found on the page.")
            return [], [], [], [], [], [], [], []
        # scroll_to_end(driver, increment=0.1)
        print(f"===== Found {len(results_items)} job items.")

        title, date, logo, company, salary, jobid, location, skills = [], [], [], [], [], [], [], []

        for item in results_items:
            try:
                job_title_element = item.find_element(By.TAG_NAME, "article")
                job_classes = job_title_element.get_attribute('class')

                if 'job--featured' in job_classes:
                    print("-- Skipping featured job.")
                    continue

                job_title = job_title_element.get_attribute('data-job-title')
                
                timestamp = job_title_element.get_attribute('data-job-posted')[:16]
                dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
                posted_date = dt_object.strftime("%m/%d/%Y %I:%M")

                company_name = job_title_element.get_attribute('data-company-name')
                salary_range = job_title_element.get_attribute('data-job-salary')
                if not salary_range:
                    salary_range = 0
                job_id = job_title_element.get_attribute('data-job-id')
                location_single = job_title_element.get_attribute('data-job-location')

                # logo
                logo_src = get_job_logo(item, job_id, job_title)

                skills_per_job = getskills(driver, jobid=job_title_element.get_attribute('data-job-id'), tools_list=tools_list)
                title.append(job_title)
                date.append(posted_date)
                logo.append(logo_src)
                company.append(company_name)
                salary.append(salary_range)
                jobid.append(job_id)
                location.append(location_single)
                skills.append(skills_per_job)
                print(f"Extracted job: {job_id}|{job_title}|{company_name}")
            except Exception as e:
                print(f"==== Error processing job for: {e}")
        
        return title, date, logo, company, salary, jobid, location, skills
            

    except Exception as e:
        print(f"==== Error in get_job_details: {e}")
        return [], [], [], [], [], [], [], []