from time import sleep

from selenium.webdriver.common.by import By
from src import utils
from src import logging


class Linkedin:

    def __init__(self):

        self.logging = logging.Logging()  # Create instance of Logging class

        url = "https://www.linkedin.com/login"
        self.driver = utils.Browser(url=url).open()  # Open the browser
        self.driver.implicitly_wait(10)  # Wait 10 seconds

    def login(self, user, pwd):
        try:

            # Send the username
            self.driver.find_element(By.ID, "username").send_keys(user)

            # Send the password
            self.driver.find_element(By.ID, "password").send_keys(pwd)

            # Click in the button
            self.driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()

            current_url = self.driver.current_url  # Get the current url
            sleep(5)
            if 'feed' not in current_url:
                self.logging.info('Error to login!')
                return 'Error to login!', False

            self.logging.info('Login successfully!')  # Logging the login successfully
            return 'Login successfully!', True  # Return the message and True
        except Exception as e:
            self.logging.error(e)  # Logging the error
            return 'Error to login!', False  # Return the message and False

    def search_collaborator(self, collaborator):
        try:

            # Clear the input
            self.driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input").clear()

            # Send the name of collaborator and press Enter
            self.driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input").send_keys(collaborator.name + u'\ue007')

            # Find the ul element
            ul_element = self.driver.find_element(By.XPATH, '//div[@class="search-results-container"]//ul')

            # Find the li elements
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

            # Iterate over the li elements
            for li in li_elements:
                if collaborator.name in li.text:  # If the name of collaborator is in the li element

                    # Find the actions
                    actions = self.driver.find_element(By.CSS_SELECTOR, ".search-nec__hero-kcard-v2-actions").find_elements(By.TAG_NAME, 'a')

                    # Click in the first action
                    actions[0].click()

                    self.logging.info(f'Collaborator {collaborator.name} found!')  # Logging the collaborator found
                    return f'Collaborator {collaborator.name} found!', True  # Return the message and True

            self.logging.info(f'Collaborator {collaborator.name} not found!')  # Logging the collaborator not found
            return f'Collaborator {collaborator.name} not found!', False  # Return the message and False
        except Exception as e:
            self.logging.error(e)  # Logging the error
            return 'Error to search collaborator!', False  # Return the message and False

    def search_description(self, collaborator):
        try:
            main = self.driver.find_element(By.CSS_SELECTOR, ".scaffold-layout__main")
            sleep(2)
            sections = main.find_elements(By.TAG_NAME, 'section')
            for section in sections:
                if 'Sobre' in section.text:
                    collaborator.description = section.text.replace('Sobre\n', '')
                    self.logging.info(f'Description of {collaborator.name} found!')  # Logging the description found
                    return f'Description of {collaborator.name} found!', True

            self.logging.info(f'Description of {collaborator.name} not found!')  # Logging the description not found
            return f'Description of {collaborator.name} not found!', False  # Return the message and False

        except Exception as e:
            self.logging.error(e)  # Logging the error
            return f'Error to search description of {collaborator.name}!', False  # Return the message and False

    def search_office_and_company(self, collaborator):
        try:
            main = self.driver.find_element(By.CSS_SELECTOR, ".scaffold-layout__main")
            sleep(2)
            sections = main.find_elements(By.TAG_NAME, 'section')
            for section in sections:
                if collaborator.name in section.text:
                    div_office = section.find_element(By.CSS_SELECTOR, ".text-body-medium")
                    div_company = section.find_element(By.CSS_SELECTOR, ".pv-text-details__right-panel")
                    collaborator.office = div_office.text.split('at')[0]
                    collaborator.company = div_company.text.split('\n')[0]

                    self.logging.info(f'Office and company of {collaborator.name} found!')  # Logging the office and company found
                    return f'Office and company of {collaborator.name} found!', True  # Return the message and True

            self.logging.info(f'Office and company of {collaborator.name} found!')  # Logging the office and company found
            return f'Office and company of {collaborator.name} found!', True  # Return the message and True

        except Exception as e:
            self.logging.error(e)  # Logging the error
            return f'Error to search office and company of {collaborator.name}!', False  # Return the message and False
