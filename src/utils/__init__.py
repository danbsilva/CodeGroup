from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:

    def __init__(self, url=None):
        self.url = url

    def open(self) -> object:
        options = webdriver.ChromeOptions()  # Create instance of ChromeOptions class
        options.add_experimental_option("excludeSwitches", ['enable-automation'])  # Exclude the enable-automation

        service = Service(ChromeDriverManager().install())  # Create instance of Service class

        driver = webdriver.Chrome(options=options, service=service, keep_alive=True)
        driver.maximize_window()  # Maximize the window
        driver.get(self.url)  # Open the url

        return driver  # Return the driver
