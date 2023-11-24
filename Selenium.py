def selenium(url):

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    # Set up the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)

    driver_path = "C:/Users/Charles/OneDrive/Documents/chromedriver-win64/chromedriver.exe"  # Replace with the path to your chromedriver executable
    chrome_service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Navigate to the webpage
    driver.get(url)

    # Wait for dynamic content to load (you may need to adjust the wait time)
    driver.implicitly_wait(10)

    # Extract the HTML content after JavaScript execution
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    return page_source

