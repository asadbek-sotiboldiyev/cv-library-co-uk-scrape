import google.generativeai as genai
import time
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
ai_model = str(os.getenv("GEMINI_MODEL"))
genai.configure(api_key=key)
def identify_title(titles, skills):
    print("===== Calling to AI =====")
    print("Titles:", titles)
    print("Skills:", skills)
    prompt = f"""

### Main rule
 You are a job title matching engine.
 Your ONLY function is to analyze the provided job titles, skills,
 and target titles. You must find the best match for each title in the 
 'job_titles' list using the 'required_skills_for_job'. 
 If you cannot confidently make a match, use 'unknown'. 
 The output MUST be a single string containing 
 ONLY the matched titles (or 'unknown') separated by commas,
 with NO spaces after the commas, 
 and NO other text, explanation, 
 or punctuation whatsoever. 
 The number of output elements must 
 EXACTLY match the number of input job titles. For example, 
 if the input job_titles has 3 items,
 the output must have 3 comma-separated items.
### Predefined Job Titles (Valid Outputs Only):
- Backend developer
- Frontend developer
- Data analyst
- Data engineer
- Data scientist
- AI engineer
- Android developer
- IOS developer
- Game developer
- DevOps engineer
- IT project manager
- Network engineer
- Cybersecurity Analyst
- Cloud Architect
- Full stack developer
- QA engineer
### Example Output:
Return the matched job_titles as a comma-separated list, maintaining the same order as the input titles. For example:
- Input: job_titles=["Junior Developer", "Data Specialist"], required_skills_for_job=["php,laravel,sql", "power bi,sql,python"]
- Output: "Backend developer, Data analyst"
### REAL Input:
- job_titles: {titles}
- required_skills_for_job: {skills}
"""
    # return titles
    try:
        # Create a generative model
        model = genai.GenerativeModel(ai_model)
        
        # Generate content using the prompt
        #print(titles)
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        output_list = [item.strip() for item in output_text.split(",")]
        #print(output_list) # uncomment for debugging
        print(output_list)
        print("===== AI work is end =====")
        time.sleep(1)
        return output_list

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("===== AI work is end =====")

        return ["unknown"] * len(titles)


def processdf(df: pd.DataFrame, chunk_size=10):

    results = []
    for i in range(0, len(df), chunk_size):

        chunk = df.iloc[i:i+chunk_size]
        titles = chunk["Job Title"].tolist()
        skills = chunk["Skills"].tolist()
        matched_titles = identify_title(titles, skills)
        if len(matched_titles) == len(titles):
            results.extend(matched_titles)
        else:
            results.extend(["invalid_ai_response"] * len(titles))
            print("> AI has returned invalid response")
            print(">>>", matched_titles)
        time.sleep(5)
    return results

def filtercolumns(df: pd.DataFrame, keywordlist: list):
    results = processdf(df, 10)
    try:
        df["Job Title from List" ] = results
        try:
            df['Salary Info'] = df['Salary Info'].fillna(0)  
            df = df.fillna('Unknown')
        except:
            pass
        # with unknown
        # df = df[df["Job Title from List"].isin(keywordlist)]

        # without unknown
        df = df[df["Job Title from List"].isin(keywordlist) & (df["Job Title from List"] != "unknown")]
        return df
    except Exception as e:
        print(f"error while filtering columns: {e}")