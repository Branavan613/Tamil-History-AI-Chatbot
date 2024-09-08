from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import math
import requests
import os

# Set up the Selenium WebDriver (using ChromeDriver in this example)
driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH or specify its location

# Open the web page
driver.get('https://documents.un.org/')  # Replace with the actual URL

# Allow the page to load
time.sleep(2)  # Adjust sleep time as needed based on page load time

# Use Selenium to find the input field and button
input_field = driver.find_element(By.ID, 'title')  # Replace with the actual ID or other selector
print(input_field)
button = driver.find_element(By.ID, 'btnSearch')  # Replace with the actual ID or other selector

# Change the content of the input field
input_field.clear()  # Clear existing content
input_field.send_keys('tamil')  # Enter new content

# Scroll to the button
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

time.sleep(1)  # Adjust sleep time as needed


# Click the button
button.click()

time.sleep(2)

first_span = driver.find_element(By.CSS_SELECTOR, '.search-criteria > span')

pagenum = int(first_span.find_elements(By.TAG_NAME, "b")[-1].text)

# Allow time for the page to update or navigate (if needed)
def next():
      # Adjust sleep time as needed

    span_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='Navigate to next page']"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    span_element.click()

    time.sleep(2)

# Use BeautifulSoup to parse the updated page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

links = []

def linkpull():
    
    # Example: Find all links with a specific class (adapt as needed)
    search_items = soup.find_all('div', class_='search-results-item')

    # Initialize a list to hold the links

    # Loop through each container
    for search_item in search_items:
        # Find all <a> elements with the class 'icofont-ui-file' within the container
        symbol = search_item.find("div", class_="symbol")
        container = symbol.find("div", class_="text-align-container")
        link = container.find('a', class_='icofont-ui-file')
        
        link_names = search_item.find_all('h2')

        # Loop through each <a> element and get the href attribute
        links.append([link_names[-1].text, link.get('href')])

        

linkpull()
for page in range(math.ceil(pagenum/20)-1):
    next()
    linkpull()
    
    # Print the links

print(links)
metadata = []
for link in links:
    # URL of the PDF file
    url = link[-1]
    print(url)
    name = link[0]
    metadata.append(name)
    name = name.split("/")[0]

    # Send a GET request to the URL
    response = requests.get(url)
    
    file_path = os.path.join("/un_documents/", name)
    # Check if the request was successful
    if response.status_code == 200:
        # Open a file to write the PDF content
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print("PDF downloaded successfully!")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
# Close the WebDriver

driver.quit()