def get_page_sel(url):
    import logging
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    # Set up the Chrome driver
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)

    driver_path = "C:/Users/Charles/OneDrive/Documents/chromedriver-win64/chromedriver.exe"  # Replace with the path to your chromedriver executable
    chrome_service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

 #   except Exception as e:
  #      print(f"Error: {e}")

    # Navigate to the webpage
    logging.info("Getting URL in chrome")
    driver.get(url)
    time.sleep(5) # should probably use implicitly_wait but can't find a way to make it work.

    # Wait for dynamic content to load (you may need to adjust the wait time)
 #   driver.implicitly_wait(20) #does not work for now, using sleep instead

    # Extract the HTML content after JavaScript execution
    page_source = driver.page_source

    # Close the browser
    driver.quit()

    logging.info("Writting text file")
    with open('C:/Users/Charles/OneDrive/Documents/GitHub/TeleComp/output/html_after_clientside_js.txt', 'w', encoding='utf-8') as f: # save a txt file with the code to make sure JS was executed as wanted
        f.write(page_source)

    return page_source
