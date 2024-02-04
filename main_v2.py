import requests
import time
from datetime import datetime
from googlesearch import search
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gforms import Form
from gforms.elements import Short, Value
from functools import partial
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import os

os.environ["LANGCHAIN_HANDLER"] = "langchain"

driver = webdriver.Chrome()

def categorize_news(body_content):
    # Define keywords or patterns for each category
    categories = {
        "Politics": ["politics", "election", "modi", "government", "democracy", "policy", "politician"],
        "International News": ["international", "world", "global", "diplomacy", "conflict", "foreign affairs", "UN"],
        "National News": ["national", "government", "country", "domestic", "policy", "leadership", "citizens"],
        "Local News": ["local", "town", "community", "neighborhood", "municipality", "events", "city council"],
        "Business and Finance": ["business", "finance", "economy", "market", "investment", "stocks", "entrepreneurship"],
        "Science and Technology": ["science", "technology", "innovation", "invented", "invent", "research", "discoveries", "AI", "robotics"],
        "Health and Wellness": ["health", "wellness", "medical", "medicine", "fitness", "nutrition", "mental health", "gym"],
        "Entertainment": ["actress", "actor", "bollywood", "tollywood", "film", "tv", "television", "stage", "hollywood", "celebrities", "music", "arts"],
        "Sports": ["cricket","sports", "athletics", "games", "competitions", "athletes", "teams", "championships"],
        "Lifestyle and Features": ["lifestyle", "features", "culture", "fashion", "travel", "food", "arts"],
        "Opinion and Editorial": ["opinion", "editorial", "commentary", "column", "op-ed", "analysis", "perspective"],
        "Environment": ["environment", "climate", "sustainability", "nature", "conservation", "ecology", "green energy"],
        "Education": ["education", "schools", "learning", "students", "teachers", "curriculum", "online learning"],
        "Crime and Justice": ["crime", "justice", "law", "police", "court", "criminal", "investigation"],
        "Human Interest": ["human interest", "human stories", "empathy", "inspiring stories", "personal narratives"],
        "Obituaries": ["obituaries", "tributes", "memorials", "remembrance", "legacy", "funeral"],
        "Weather": ["weather", "forecast", "climate", "meteorology", "seasons", "natural disasters"],
        "Religion and Spirituality": ["religion", "spirituality", "faith", "belief", "rituals", "religious practices"],
        "Technology and Gadgets": ["technology", "gadgets", "electronics", "devices", "innovations", "wearables"],
        "Automotive": ["automotive", "cars", "vehicles", "car industry", "motorcycles", "automobile technology"]
    }

    # Convert the content to lowercase for case-insensitive matching
    content_lower = body_content.lower()

    # Initialize a dictionary to count occurrences of keywords for each category
    category_counts = {category: 0 for category in categories}

    # Count occurrences of keywords for each category
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in content_lower:
                category_counts[category] += 1

    # Get the category with the highest count (most relevant category)
    max_count_category = max(category_counts, key=category_counts.get)

    if category_counts[max_count_category] > 0:
        return max_count_category
    else:
        # If no specific category is found, return a default category or None
        return "National News"  # Change this default value if needed

def FillForm(headline,bodyorcontent,HumanSummary,category,newspaper,date):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdAJTmn_VNI5YPuhv9f62uhd4KG3f8FZezT9-BYndsbCdkmKQ/viewform"  # Replace with your Google Form URL
    driver.get(form_url)
    time.sleep(1)

    # Fill the form fields
    input_field_1 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_field_1.send_keys("Abhishek Sharma")

    input_field_2 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_field_2.send_keys(newspaper)

    input_field_3 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
    input_field_3.send_keys(date)
    
    input_field_4 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_field_4.send_keys(headline)

    input_field_5 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div[2]/textarea')
    input_field_5.send_keys(bodyorcontent)
    
    input_field_6 = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div[2]/textarea')
    input_field_6.send_keys(HumanSummary)

    #category choose
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[text()='{category}']"))
    )

    # Check if the option matches the variable, then click on it
    if element.text == category:
        element.click()
        print(f"Selected {category}")
    else:
        element.click()
    # Submit the form
    # time.sleep(100)
    submit_button = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(0.1)

    # Close the browser after a short delay

    # driver.quit()

def GetTopics():
    # Open the file in read mode ('r')
    file_path = 'TopicList.txt'  # Replace with your file path
    result = []
    with open(file_path, 'r') as file:
        # Read the file line by line
        for line in file:
            result.append(line.strip())
    return result

def Body_TT(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('article', id='contentbox')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove extra line spaces and "ADVERTISEMENT" term
            result_cleaned = result.replace("\n\n", "\n").replace("ADVERTISEMENT", "")
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result_cleaned if ord(char) < 128)
            # Get content before "Read more" term if present
            read_more_index = result_cleaned.find("READ ALSO")
            if read_more_index != -1:
                result_cleaned = result_cleaned[:read_more_index]
            return result_cleaned.strip()
        else:
            print('Article body element not found.')
            return result
    else:
        print('Failed to fetch the URL.')
        return ""


def Date_TT(url):
    response = requests.session()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        date_element = soup.find('div', class_='publishdate mt-32')
        date_string = date_element.text.strip()
        if date_element:
            date_string = date_element.text.strip()
            
            # Regular expression to match the published date pattern
            date_pattern = r'Published (\d{1,2}.\d{1,2}.\d{2}), \d{1,2}:\d{2} [APM]{2}'
            
            # Try to extract the published date string
            match = re.search(date_pattern, date_string)
            if match:
                published_date = match.group(1)
                try:
                    # Parse the extracted published date string into a datetime object
                    published_date_obj = datetime.strptime(published_date, '%d.%m.%y')
                    
                    # Format the datetime object to the desired format 'dd/mm/yyyy'
                    formatted_published_date = published_date_obj.strftime('%d/%m/%Y')
                    
                    return formatted_published_date
                except ValueError:
                    print("Failed to parse date.")
                    return None
            else:
                print("Published date pattern not found.")
                return None
        else:
            print('Date element not found.')
            return None
    else:
        print('Failed to fetch the URL.')
        return None


def headline_TT(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('h1', class_='')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result if ord(char) < 128)
            return result_cleaned
        else:
            print('Article body element not found.')
            return result

def Body_TOI(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='_s30J clearfix')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result if ord(char) < 128)
            return result_cleaned
        else:
            print('Article body element not found.')
            return result


def Date_TOI(url):
    response = requests.session()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        date_element = soup.find('div', class_='xf8Pm byline')
        
        if date_element:
            date_string = date_element.text.strip()
            
            # Regular expressions to match different date patterns
            date_patterns = [
                r'Updated: (\w+ \d{1,2}, \d{4}, \d{1,2}:\d{2})',
                r'(\w+ \d{1,2}, \d{4}), \d{1,2}:\d{2}',
                r'(\w+ \d{1,2}, \d{4})'
            ]
            
            # Try each pattern to extract the date string
            for pattern in date_patterns:
                match = re.search(pattern, date_string)
                if match:
                    extracted_date = match.group(1)
                    try:
                        # Parse the extracted date string into a datetime object
                        date_object = datetime.strptime(extracted_date, '%b %d, %Y')
                        
                        # Format the datetime object to the desired format 'dd/mm/yyyy'
                        formatted_date = date_object.strftime('%d/%m/%Y')
                        return formatted_date
                    except ValueError:
                        continue  # Try the next pattern if parsing fails
                    
            print("Failed to parse date.")
            return None
        else:
            print('Date element not found.')
            return None
    else:
        print('Failed to fetch the URL.')
        return None


def headline_TOI(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('h1', class_='HNMDR')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result if ord(char) < 128)
            return result_cleaned
        else:
            print('Article body element not found.')
            return result

def Body_DC(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='details-info')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result if ord(char) < 128)
            return result_cleaned
        else:
            print('Article body element not found.')
            return result


def Date_DC(url):
    response = requests.session()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        date_element = soup.find('div', class_='text-gray text-small')
        date_string = date_element.text.strip()
        if date_element:
            date_string = date_element.text.strip()
            
            # Regular expression to match the published date pattern
            date_pattern = r'Published on: (\w+ \d{1,2}, \d{4}) \| Updated on:'
            
            # Try to extract the published date string
            match = re.search(date_pattern, date_string)
            if match:
                published_date = match.group(1)
                try:
                    # Parse the extracted published date string into a datetime object
                    published_date_obj = datetime.strptime(published_date, '%B %d, %Y')
                    
                    # Format the datetime object to the desired format 'dd/mm/yyyy'
                    formatted_published_date = published_date_obj.strftime('%d/%m/%Y')
                    
                    return formatted_published_date
                except ValueError:
                    print("Failed to parse date.")
                    return None
            else:
                print("Published date pattern not found.")
                return None
        else:
            print('Date element not found.')
            return None
    else:
        print('Failed to fetch the URL.')
        return None


def headline_DC(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('h1', class_='')
        result = ""
        if article_body:
            result = article_body.text.strip()
            # Remove problematic characters
            result_cleaned = ''.join(char for char in result if ord(char) < 128)
            return result_cleaned
        else:
            print('Article body element not found.')
            return result


def TextGeneration(body):
    summary = summarize(body, word_count=100)
    return summary

urls = GetTopics()
formfilled = 0
# Inside the loop where you fetch URLs

for url in urls:
    try:
        if 'telegraphindia' in url:
            body = Body_TT(url)
            headline = headline_TT(url)
            date = Date_TT(url)
            category = categorize_news(body)
            HumanSummary = TextGeneration(body)
            FillForm(headline, body, HumanSummary, category, 'The Telegraph', date)
            formfilled+=1
        if 'timesofindia' in url:
            body = Body_TOI(url)
            headline = headline_TOI(url)
            date = Date_TOI(url)
            category = categorize_news(body)
            HumanSummary = TextGeneration(body)
            FillForm(headline, body, HumanSummary, category, 'Times of India', date)
            formfilled+=1
        if 'deccanchronicle' in url:
            body = Body_DC(url)
            headline = headline_DC(url)
            date = Date_DC(url)
            category = categorize_news(body)
            HumanSummary = TextGeneration(body)
            FillForm(headline, body, HumanSummary, category, 'Deccan Chronicle', date)
            formfilled+=1
    except Exception as e:
        print(f"Error processing URL: {url}")
        print(f"Error details: {str(e)}")

        driver.get(url)

        # Add your form-filling logic here
        # For example, locating and interacting with form elements
        # ...

        # Check if an alert is present
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert

        # If the alert is present, handle it by choosing 'Leave'
        if 'Leave' in alert.text:
            alert.dismiss()

print("Form Filled = " + formfilled)