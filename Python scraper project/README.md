# Instruction

Beautiful Soup

To run the code, you need to download and open the bs4_parser.py file in the code editor. And run the code, you can also choose the number of pages or remove the page limit altogether.

Scrapy

Firstly to run the code, you need to download the otodom_scraper file.

In order to start parsing Scary you need:
•	you will need to upload the code to the spiders folder
•	change settings.py as needed
•	and run the scrapy crawl command of two spiders: one after the end of the other

Selenium

• To run the code, you need to download the slm_parser file.

• Download chromedriver for your desired platform from here -> https://sites.google.com/a/chromium.org/chromedriver/downloads
• Place chromedriver on your system path, or where your code is.
• If not using a system path, link your chromedriver.exe (For non-Windows users, it's just called chromedriver):

        browser = webdriver.Chrome(executable_path=r"C:\path\to\chromedriver.exe")
        (Set executable_path to the location where your chromedriver is located.)
        
        If you've placed chromedriver on your System Path, you can shortcut by just doing the following:
        browser = webdriver.Chrome()
• If you're running on a Unix-based operating system, you may need to update the permissions of chromedriver after downloading it in order to make it executable:
        
        chmod +x chromedriver

• And run the code


Source: https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver
