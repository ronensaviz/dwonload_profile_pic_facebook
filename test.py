from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Define the URL of the Facebook album
album_url = "https://www.facebook.com/media/set/?set=a.165916470091759&type=3"

# Specify the path to the ChromeDriver executable (download it from https://sites.google.com/chromium.org/driver/)
chrome_driver_path = "/path/to/chromedriver"

# Create a Chrome WebDriver with cookies loaded from the cookies.txt file
driver_service = ChromeService(chrome_driver_path)
driver = webdriver.Chrome(service=driver_service)

# Open the album URL
driver.get(album_url)

# Read cookies from a text file
cookies = {}
with open("cookies.txt", "r") as cookie_file:
    for line in cookie_file.read().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            key, value = parts[0], parts[1]
            cookies[key] = value

# Add cookies to the browser session
for key, value in cookies.items():
    driver.add_cookie({"name": key, "value": value})

# Refresh the page to apply cookies
driver.refresh()

# Wait for the page to load (you may need to adjust the waiting time)
driver.implicitly_wait(10)  # Adjust the waiting time as needed

# Find all image elements using their class (you might need to inspect the page to find the correct class)
image_elements = driver.find_elements(By.CLASS_NAME, "your-image-class")

# Extract the image URLs from the "src" attribute
image_urls = [img.get_attribute("src") for img in image_elements]

# Print the extracted image URLs
for url in image_urls:
    print(url)

# Close the browser
driver.quit()
