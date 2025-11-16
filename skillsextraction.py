from selenium.webdriver.common.by import By
import re

def getskills(driver, jobid, tools_list):
    try:
        pageurl = f'https://www.cv-library.co.uk/job/{jobid}'
        # Open a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get(pageurl)

        try:
            elements = driver.find_elements(By.CLASS_NAME, "job__description")
            skills = []
            for element in elements:
                element_text = element.text

                for skill in tools_list:
                    if re.search(rf'\b{re.escape(skill)}\b', element_text, re.IGNORECASE) and skill not in skills:
                        skills.append(skill)
            # Close the new tab
            driver.close()

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])
            return skills
        except:
            print('==== Error during get skills')

    except:
        print('==== url error')
        pass
    
