# News Article Categorization and Summarization

## Overview
This Python project aims to automate the categorization and summarization of news articles from various news websites. The program utilizes web scraping techniques to extract article content, headlines, and publication dates. It then employs natural language processing (NLP) techniques to categorize the news articles into predefined categories and generate human-readable summaries.

## Features
- **Web Scraping:** The project uses the BeautifulSoup library to scrape article content, headlines, and dates from popular news websites such as The Telegraph, Times of India, and Deccan Chronicle.
- **Text Categorization:** The program employs keyword matching to categorize news articles into predefined categories such as Politics, Business, Science, Entertainment, and more.
- **Text Summarization:** The Gensim library is used for automatic text summarization to generate concise summaries of the news articles.
- **Google Forms Integration:** The project includes functionality to automatically fill out a Google Form with relevant information extracted from the news articles, such as headline, content, category, and date.

## Dependencies
Make sure you have the following Python libraries installed:
- requests
- beautifulsoup4
- gensim
- scikit-learn
- googlesearch-python
- gforms
- selenium

You can install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

## Usage
1. Add URLs of news articles to the `TopicList.txt` file.
2. Run the script to categorize and summarize the news articles.
3. The program will automatically fill out a Google Form with relevant information.

Note: Make sure to set up your Chrome WebDriver for Selenium by providing the correct path.

## Customization
- Modify the `categories` dictionary in the code to add or modify news categories and their associated keywords.
- Adjust the default category in the `categorize_news` function if needed.

## Contributors
- Abhishek Sharma
