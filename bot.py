from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchFrameException, \
    TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import ActionChains
from dotenv import load_dotenv
from datetime import datetime, timedelta, time as dtime
from random import randint
from utils import send_message_to_private_channel
import pickle
import os
import time
import logging

load_dotenv()


class MidlandBot:

    def __init__(self, user_name, password, monitoring_id, ni_number, start, end):
        self.username = user_name
        self.password = password
        self.home_page = "https://homes.midlandheart.org.uk/"
        self.tab_before_login = ""
        self.start_time = start
        self.end_time = end
        self.user_ni_number = ni_number
        self.listing_id = monitoring_id
        self.listings_for_today = []
        self.logger = logging.getLogger("Midland_logger")
        self.logger.setLevel(logging.INFO)  # Set the desired logging level for this class
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        # Create a StreamHandler to log to console (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create a FileHandler to log to a file (optional)
        file_handler = logging.FileHandler(f'{user_name}_{monitoring_id}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Initialize Chrome Driver
        self.driver = self.initialize_chrome_driver()
        self.action = ActionChains(self.driver)

        # open homepage
        self.driver.get(self.home_page)
        self.logger.info("Bot is starting...")

    @staticmethod
    def initialize_chrome_driver():
        """
        Initializes the Chrome Driver and then returns the driver object.
        :return: The Chrome Driver
        :rtype:
        """

        # Create Chrome options instance
        options = Options()

        # Add My chrome profile
        # options.add_argument(r"--user-data-dir=C:\\Users\\Windows\\AppData\\Local\\Google\\Chrome\\User Data")
        # options.add_argument(r'--profile-directory=Default')

        options.add_argument("--start-maximized")

        # Adding argument to disable the AutomationControlled flag
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Exclude the collection of enable-automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Turn-off userAutomationExtension
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')

        # Run in the headless browser
        options.headless = True

        # Set this to make it work with the docker container
        options.add_argument('--disable-gpu')
        # options.add_argument('--remote-debugging-port=9222')

        # Setting the driver path and requesting a page
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Changing the property of the navigator value for webdriver to undefined
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    def login_with_cookies(self):
        """
        This method returns a True or False Depending on whether the login with cookies was successful
        :return:
        :rtype:
        """
        # Check to see if the cookies we loaded in the beginning worked, else return false
        if self.login_success():
            return True

        else:
            pass
        self.driver.refresh()
        time.sleep(2)
        # First Try to load cookies before logging in then login if the cookies is not available
        try:
            self.logger.info("Attempting to Load cookies..")
            self.load_cookie_session()
            self.driver.get(self.home_page)
            time.sleep(2)

        except FileNotFoundError:
            self.logger.info("Cookies not found...")

            return False

        return self.login_success()

    def sleep_until_9am(self):
        current_time = datetime.now().time()
        start_time = dtime(0, 0)
        target_time = dtime(9, 0)

        if start_time <= current_time < target_time:
            sleep_seconds = (target_time.hour - current_time.hour) * 3600 + (
                        target_time.minute - current_time.minute) * 60
            self.logger.info(f"Waiting for {sleep_seconds} seconds...")
            time.sleep(sleep_seconds)

            self.logger.info("It's 9:00 AM!")

        else:
            self.logger.info("It's already past 9:00 AM!")

    def send_message_to_telegram(self, message):
        # Replace with your bot token and the private channel's username
        bot_token = os.getenv("BOT_TOKEN")
        private_channel_username = os.getenv("BOT_USERNAME")  # Replace with the private channel's username
        recipient_user_id = "RECIPIENT_USER_ID"  # Replace with the User ID of the recipient

        # Send the message to the private channel
        result = send_message_to_private_channel(bot_token, private_channel_username, message)
        if result:
            self.logger.info("Message sent to monitoring channel successfully!")
        else:
            self.logger.info("Failed to send message to monitoring channel.")

    def login_to_website(self):
        """
        This method logs in to the website using the Username and Password after clicking the login button.
        """
        # self.open_login_tab()
        # Try to load cookies before logging in then login if the cookies is not available
        # cookies_success = self.login_with_cookies()

        time.sleep(randint(0, 4))

        # Open Login URL
        self.driver.get('https://homes.midlandheart.org.uk/Login.aspx')
        time.sleep(3)
        try:
            self.logger.info("Attempting to login to website...")
            # Enter Email Address
            email = self.driver.find_element(By.XPATH, '//input[@type="email"]')
            self.interact_and_type(email, self.username)

            # Enter Password
            password = self.driver.find_element(By.XPATH, '//input[@type="password"]')
            self.interact_and_type(password, self.password)

            # Click Login Button
            submit_login_button = self.driver.find_element(By.XPATH, '//input[@type="submit"]')
            self.interact_and_click(submit_login_button)

        except NoSuchElementException:
            self.logger.info("Failed to Login To Website..")
            time.sleep(2)

        # Save Cookies if the login was successful
        if self.login_success():
            time.sleep(3)

            # # Delete existing cookies and save new cookies
            # self.delete_cookie_file()
            # # Attempt to save cookies
            # self.save_cookie_session()

        # self.close_login_tab()

        return self.login_success()

    def login_success(self):
        """
        Checks to see if the Website has succesfully logged in and then returns True or False depending on the condition

        :return: True if successful, False otherwise
        :rtype: Boolean
        """
        # self.driver.get(self.home_page)
        # time.sleep(2)
        try:
            time.sleep(1)
            self.logger.info("Checking if user is logged in...")
            self.driver.find_element(By.XPATH, '//span[@class="fa fa-fw fa-user"]')

        except NoSuchElementException:
            self.logger.info("User not Logged in...")
            return False

        else:
            self.logger.info("User is Logged in...")
            return True

    def open_login_tab(self):
        """
        Opens a new tab and then logs into that new tab an
        :return:
        :rtype:
        """
        # Get the ID of the current window
        self.tab_before_login = self.driver.current_window_handle
        self.driver.execute_script(f'''window.open("{self.home_page}","_blank");''')
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # Switch to the last tab on the list which most times is the newly opened tab.
        # self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_login_tab(self):
        # Close the new tab
        self.driver.close()

        # Switch back to the original tab
        self.driver.switch_to.window(self.tab_before_login)
        time.sleep(1)
        # Refresh the page in the original tab
        self.driver.refresh()

    def save_cookie_session(self):
        # Save the cookie session id
        pickle.dump(self.driver.get_cookies(), open("midland_cookies.pkl", "wb"))
        self.logger.info("Cookies saved successfully...")

        self.extend_cookies()

    def load_cookie_session(self):
        # load Cookies from saved session

        try:
            cookies = pickle.load(open("midland_cookies.pkl", "rb"))

            for cookie in cookies:
                self.driver.add_cookie(cookie)
                self.logger.info('loading cookie')
            self.logger.info("Loaded cookies from previous session...")

            self.driver.refresh()

        except FileNotFoundError:
            self.logger.info('Could not find Cookies file...')

    def extend_cookies(self):
        cookie_file_path = 'midland_cookies.pkl'

        # Check if the cookie file exists
        if os.path.exists(cookie_file_path):
            with open(cookie_file_path, 'rb') as f:
                cookies = pickle.load(f)

            # Calculate the new expiration time (current expiration + 7 days)
            for cookie in cookies:
                if 'expiry' in cookie:
                    current_expiry = cookie['expiry']
                    new_expiry = current_expiry + (7 * 24 * 60 * 60)  # Add 7 days in seconds
                    cookie['expiry'] = new_expiry

            # Save the updated cookies to the same file
            with open(cookie_file_path, 'wb') as f:
                pickle.dump(cookies, f)

            self.logger.info("Cookies expiration extended successfully.")
        else:
            self.logger.info("Cookie file not found. Make sure to save the cookies first.")

    def delete_cookie_file(self):
        cookie_file_path = 'midland_cookies.pkl'
        if os.path.exists(cookie_file_path):
            os.remove(cookie_file_path)
            self.logger.info(f"Deleted the cookie file: {cookie_file_path}")
        else:
            self.logger.info("Cookie file does not exist.")

    def get_results_for_city(self, city="Birmingham", mile_radius=20):
        """
        This function opens the page containing all the results for the given city and the mile radius
        :param city: Enter the name of the city you'll like to search for,Set to Birmingham by default
        :type city: String
        :param mile_radius: How many mile radius from the city? set to 20 by default.
        :type mile_radius: int
        """
        # FFind the search button and pass the city through
        try:
            self.logger.info("Searching for search button")
            search_field = self.driver.find_element(By.XPATH,
                                     '//input[@id="MidlandHeartWeb_Theme_wt209_block_OutSystemsUIWeb_wt2_block_wtContent_wtMainContent_OutSystemsUIWeb_wt83_block_wtContent_OutSystemsUIWeb_wt174_block_wtInput_wtInput_SearchTerms"]')

            search_field.send_keys(city)
            self.logger.info(f"Entered {city} in the search button")
            # click the search button

            search = self.driver.find_element(By.XPATH, '//span[@class="fa fa-fw fa-search"]')
            self.interact_and_click(search)
            time.sleep(2)
            # Add the mile radius to the search
            self.confirm_city_mile_radius()

        except NoSuchElementException:
            self.logger.info("Failed to locate search...")
            pass

    def confirm_city_mile_radius(self):
        try:
            select_miles = self.driver.find_element(By.XPATH,
                                                    '//select[@class="select OSFillParent"]')
            self.interact_and_click(select_miles)
            # choose 20 miles
            mile_number = self.driver.find_element(By.XPATH, '//option[@value="9"]')
            self.interact_and_click(mile_number)

            submit_prop = self.driver.find_element(By.XPATH, '//input[@value="Show properties"]')
            self.interact_and_click(submit_prop)

        except NoSuchElementException:
            self.logger.info("Failed to locate Birmingham on new page")

    def get_all_listings(self):
        all_listings = self.driver.find_elements(By.XPATH, '//div[@class="property-body"]')
        # self.logger.info(f"Retrieved {len(all_listings)} listings...")

        return all_listings

    def get_listings_for_today(self):
        today = datetime.now()
        sample_date = today
        valid_listings = []

        # Format the date as "Day date Month" because this is the format of the date when it is not available
        today_date_1 = sample_date.strftime("%A %d %B")
        # Format the date as day/month/year so that we can check if the item is available.
        today_date_avail = sample_date.strftime("%d/%m/%Y")

        self.logger.info(f"Searching for listings for {today_date_1}...")
        try:
            all_listings = self.driver.find_elements(By.XPATH, '//div[@class="property-body"]')
            # self.logger.info(f"Found {len(all_listings)} listings...")

            for listing in all_listings:
                listing_name = listing.find_element(By.CLASS_NAME, "text-neutral-8")

                new_entry = {
                    "sel_object": listing,
                    "available": None,
                    "valid": None,
                    "name": None,
                    "pending_date": today_date_1,
                    "available_date": today_date_avail,
                    "placed_order": False
                }
                # self.logger.info(listing.text)
                listing_description = listing.find_element(By.CLASS_NAME, "text-neutral-6").text

                # self.logger.info(listing_description)
                if today_date_1 in listing_description:
                    # if the date is valid for today
                    new_entry['valid'] = True
                    new_entry['available'] = False
                    new_entry['name'] = listing_name.text

                    valid_listings.append(new_entry)

                elif today_date_avail in listing_description:
                    new_entry['valid'] = True
                    new_entry['available'] = True
                    new_entry['name'] = listing_name.text
                    valid_listings.append(new_entry)

            self.logger.info(f"Found {len(valid_listings)} / {len(all_listings)} listings for today...")
            return valid_listings

        except NoSuchElementException:
            self.logger.info("No listing found")
            return []

    def keep_checking_for_listing(self, today_listings):
        """
        THis function keeps checking the search results page to see when the description on the listing for the day changes. and then returns true
        :param today_listings: A list containing a dictionary of the valid listings for the day
        :type today_listings: list
        """
        count = 0
        listing_found = False
        self.logger.info("Scanning page for available listing...")
        # While the listing has not been found, create a while loop to keep searching
        while not listing_found and count < 50:
            # Increase the count to we monitor how many times the loop runs
            count += 1
            # Get all the listings on the page, I'm doing this so that we can get recent updates from the page
            all_listings = self.get_all_listings()

            # For each listing in all of them
            for orig_listing in all_listings:

                # Continue the loop when we encounter a listing that is not for today.
                for listing in today_listings:
                    if listing['name'] not in orig_listing.text:
                        continue
                    else:
                        if listing['available_date'] in orig_listing.text:
                            self.logger.info(f"{listing['name']} has become available... \nPreparing to place order...")
                            listing_found = True
                            return True
                        else:
                            continue

            time.sleep(2)
        return False

    def open_listing(self, name):
        all_listings = self.get_all_listings()

        for listing in all_listings:
            if name in listing.text:
                self.interact_and_click(listing)
                self.logger.info("Opening Listing...")

    def listing_page_loaded(self):
        # Wait for the listing page to load before progressing.
        self.logger.info("Waiting for listing to load...")
        self.driver.switch_to.window(self.driver.window_handles[-1])

        try:
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//span[@class="text-capitalize"]')

        except NoSuchElementException:
            return False

        return True

    def get_listing_id(self, sel_object):
        """
        Get the ID for the listing that are valid for today

        """
        # Click on listing
        self.interact_and_click(sel_object)

        # Switch to the active tab that the listing has been opened on
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # get the address and extract the listingId from the address
        self.logger.info("Obtaining Id for Listing")
        url = self.driver.current_url
        if 'PropertyId' in url:
            id = url.split("=")[-1]

            self.driver.close()
            return int(id)

        else:
            self.driver.close()
            return None

    def is_listing_available(self, id: int, waiting_timeout: int):
        """
        This function gets the listing ID of the listing to be monitored and sets a particular time to
        wait for the listing to become available.
        :param id: the listing id of the listing
        :type id: int
        :param waiting_timeout: the time in seconds to wait for the listing
        :type waiting_timeout: int
        :return: The status of the listing after the waiting timeout has elapesd
        :rtype: Boolean
        """

        if str(id) not in self.driver.current_url:
            self.driver.get(f"https://homes.midlandheart.org.uk/Search.PropertyDetails.aspx?PropertyId={id}")

        wait = WebDriverWait(self.driver, waiting_timeout)

        try:
            # Wait for either "Apply Now" button or "Submit Application" button to be visible on the page.
            apply_button = (By.XPATH, '//input[@value="Apply Now"]')
            continue_button = (By.XPATH, '//input[@value="Continue Application"]')
            self.logger.info(f"Waiting for listing {id} to become available")

            # Wait for any of the two buttons to be visible.
            visible_button = wait.until(EC.any_of(EC.presence_of_element_located(apply_button),
                                                  EC.presence_of_element_located(continue_button)
                                                  ))

            # Click the button that became visible.
            # Listing just became availble
            self.logger.info(f"Listing {id} is now available...")
            self.interact_and_click(visible_button)
            message = f"Listing https://homes.midlandheart.org.uk/Search.PropertyDetails.aspx?PropertyId={id} is now live... \nFollow URL to apply"
            self.send_message_to_telegram(message)
            self.logger.info(f"Successfully opened listing {id}... Preparing to apply...")

            # Perform the corresponding application process here (filling out forms, etc.).
            return True

        except TimeoutException:
            # If neither of the buttons becomes visible within the specified timeout (30 seconds),
            # the WebDriverWait will raise a TimeoutException, and the script will come here.
            self.logger.info(
                "Neither the Continue Application button nor the 'Submit Application' button became visible.")
            self.logger.info("Listing has not become avialable... Refreshing page...")

            return False

    @staticmethod
    def trash_button_exists(driver):
        try:
            driver.find_element(By.XPATH, '//span[@class="fa fa-fw fa-trash-o fa-2x"]')
        except NoSuchElementException:
            return False
        else:
            return True

    @staticmethod
    def get_files_uploaded(driver):
        uploads = driver.find_elements(By.XPATH, './/span[@class="fa fa-fw fa-trash-o fa-2x"]')
        # self.logger.info(uploads)
        return len(uploads)

    def get_files_available(self, driver):
        # Click the requirement and add the required file
        driver.find_element(By.XPATH, './/span[@class="heading6"]').click()
        time.sleep(5)

        # Wait till the close button in clickable
        # test_bot.button_is_clickable('//span[@class="fa fa-fw fa-close fa-2x"]', 10)
        close_buttons = driver.find_elements(By.XPATH, '//span[@class="fa fa-fw fa-close fa-2x"]')

        avail_files = self.driver.find_elements(By.XPATH, '//aside//input[@value="Add"]')
        # self.logger.info(avail_files)
        time.sleep(1)

        for i in range(len(close_buttons)):
            try:
                close_buttons[i].click()
            except:
                pass
            else:
                continue

        return len(avail_files)

    @staticmethod
    def add_nth_item(driver, index):
        # Click the card title to open the pop up for the files
        driver.find_element(By.XPATH, './/span[@class="heading6"]').click()
        time.sleep(3)

        # Get the list of available files
        avail_files = driver.find_elements(By.XPATH, '//aside//input[@value="Add"]')

        # If there are no uploaded files
        if avail_files == []:
            return False
            # Get the item in the index given
        item_to_select = avail_files[index]
        item_to_select.click()
        time.sleep(3)
        return True

    @staticmethod
    def get_all_cards(driver):
        return driver.find_elements(By.XPATH, '//div[@class="card"]')

    @staticmethod
    def card_name(card):
        return card.find_element(By.XPATH, './/span[@class="heading6"]').text

    @staticmethod
    def get_latest_file_uploaded_to_card(card):
        try:
            uploaded_span = \
            card.find_elements(By.XPATH, './/div[@class="padding-s ThemeGrid_Width6 ThemeGrid_MarginGutter"]')[-1]
            title_attribute = uploaded_span.text
            return title_attribute
        except NoSuchElementException:
            return None

    def monitor_listing(self, id: int):
        start_time = dtime(self.start_time, 0)
        end_time = dtime(self.end_time, 0)
        timeout = 20

        self.logger.info(f'Monitoring from time {self.start_time} --> {self.end_time}')
        while start_time <= datetime.now().time() <= end_time:
            if dtime(10, 30) <= datetime.now().time() <= end_time:
                timeout = 10
                self.logger.info(f"Waiting time is now {timeout}")

            time.sleep(randint(5, 10))
            status = self.is_listing_available(id=id, waiting_timeout=timeout)
            if status:
                return status

            else:
                self.driver.refresh()

    def on_error_page(self):
        if "Error" in self.driver.title:
            return True
        else:
            return False

    def on_valid_page(self, text: str):
        if text in self.driver.title:
            self.logger.info(f"Successfully loaded {text} page...")
            return True

        else:
            return False

    def upload_age_designated(self):
        # Find the age designanated Element
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Age designated households")]')
        pass

    def upload_photo_id(self):
        self.driver.find_element(By.XPATH, '//span[contains(text(), "")]')

        pass

    def interact_and_click(self, element):
        """
        This method interacts with a particular element before clicking on it.
        :param element: The element to interact with
        :type element: selenium.Element
        """
        time.sleep(randint(0, 3))
        self.action.move_to_element(element)
        time.sleep(randint(0, 3))
        element.click()

    def button_is_clickable(self, button_xpath, timeout=3):
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            return True

        except:
            return False

    def interact_and_type(self, element, text_to_enter):
        """
        This function interacts with a particular element and sends in a text to its input.
        :param element: The element to interact with
        :type element: Selenium Element
        :param text_to_enter: The text to be entered into the selenium function
        :type text_to_enter: string
        """
        time.sleep(randint(0, 3))
        self.action.move_to_element(element)
        time.sleep(randint(0, 3))
        element.send_keys(text_to_enter)

    def continue_button_clickable(self):
        return self.button_is_clickable('//input[@type="submit" and @value="Continue"]', 2)

    def get_top_cards(self):
        top_cards_con = self.driver.find_element(By.ID,
                                                     "MidlandHeartWeb_Theme_wt72_block_OutSystemsUIWeb_wt2_block_wtContent_wtMainContent_OutSystemsUIWeb_wt107_block_wtColumn1_wtGroupsList")
        # self.logger.info(top_cards_con)

        top_cards = top_cards_con.find_elements(By.XPATH, './/div[@class="margin-bottom-base"]')
        # self.logger.info(top_cards)
        return top_cards

    def click_continue_button(self):
        continue_button = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Continue"]')
        try:
            self.interact_and_click(continue_button)
        except:
            return False
        else:
            return True

    def find_property_by_address(self, address):
        """
        This function searches for a property on the listing results page and finds the preperty with that exact address
        :param address: the address of the property to be found
        :type address: string
        :return:
        :rtype:
        """

        result = self.driver.find_element(By.XPATH, f'//span[contains(text(), "{address}")]')
        return result

    def click_all_yes_on_preference_page(self):
        yes_buttons = self.driver.find_elements(By.XPATH, '//input[@type="radio" and @value="2"]')

        for i in range(len(yes_buttons)):
            all_buttons = self.driver.find_elements(By.XPATH, '//input[@type="radio" and @value="2"]')
            try:
                button = all_buttons[i]
                self.interact_and_click(button)

            except ElementNotInteractableException:
                pass

            if i <= 1:
                time.sleep(5)
            else:
                time.sleep(1)

    def check_and_click_continue_button(self):
        if self.continue_button_clickable():
            self.click_continue_button()
            next_page = self.click_continue_button()
            if next_page:
                return True
            else:
                pass

    def pass_eligibility_stage(self):
        """
        THis functions passes through the elegiility stage. and returns a boolean depending on the outcome.
        :return:
        :rtype: bool
        """
        if self.on_valid_page('Eligibility'):

            can_proceed_to_next = self.check_and_click_continue_button()
            if can_proceed_to_next:
                return True

            # Check to see if the continue button is clickable.
            continue_button = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Continue"]')
            self.logger.info("Checking to see if all the requirements have been filled...")
            if self.button_is_clickable(button_xpath='//input[@type="submit" and @value="Continue"]'):
                self.logger.info("All requirements have been filled, Clicking button to proceed to next stage...")

                self.interact_and_click(continue_button)
                return True

            else:
                return False

        return False

    def pass_preference_group(self):
        # Check if we're on the right page
        if self.on_valid_page('Preference'):
            # Check to see if the continue button is clickable.
            continue_button = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Continue"]')
            self.logger.info("Checking to see if all the Preference requirements have been filled...")
            if self.button_is_clickable(button_xpath='//input[@type="submit" and @value="Continue"]'):
                self.logger.info("All Preferences have been filled, Clicking button to proceed to next stage...")
                # The button is clickable.
                self.interact_and_click(continue_button)
                return True
            else:
                self.click_all_yes_on_preference_page()
                self.click_continue_button()

        return False

    def pass_evidence_stage(self):
        # Check to ensure that we are on teh right page
        if self.on_valid_page('Evidence'):
            time.sleep(3)
            all_top_cards = self.get_top_cards()
            self.logger.info(f"Found {len(all_top_cards)} categories of requirements")

            for u in range(len(all_top_cards)):
                can_proceed_to_next = self.check_and_click_continue_button()
                if can_proceed_to_next:
                    return True

                alll_cards = self.get_top_cards()
                active_top_card = alll_cards[u]
                self.logger.info(active_top_card.text)
                time.sleep(5)
                try:
                    self.interact_and_click(active_top_card)
                except ElementNotInteractableException:
                    pass
                # Get the individual Cards beneath the main top_card
                requirements_cards = self.get_all_cards(self.driver)
                num_of_cards = len(requirements_cards)

                for i in range(num_of_cards):
                    time.sleep(5)
                    current_card = self.get_all_cards(self.driver)[i]
                    current_card_name = self.card_name(current_card)
                    self.logger.info(f"\nCard --> {current_card_name}")
                    # self.logger.info(current_card.text)
                    files_uploaded = self.get_files_uploaded(current_card)
                    files_available = self.get_files_available(current_card)

                    if files_available == 0:
                        self.logger.info(f"No File was found for {current_card_name}")
                        continue
                    if files_uploaded >= files_available:
                        self.logger.info(f"All requirements have been fufilled for the {current_card_name} card")
                        continue
                    self.logger.info("\n")
                    self.logger.info(f"files_added : {files_uploaded} \nfiles available : {files_available}")

                    # loop through the number of available files and add each one.
                    for j in range(files_available):
                        current_card = self.get_all_cards(self.driver)[i]
                        success = self.add_nth_item(current_card, j)

                        # Check if the attempt to upload the files were succesful else
                        if success:
                            new_current_card = self.get_all_cards(self.driver)[i]
                            name_of_file_added = self.get_latest_file_uploaded_to_card(new_current_card)
                            self.logger.info(f"Successfully uploaded file: {name_of_file_added} for {current_card_name}")
                            files_uploaded += 1
                        else:
                            self.logger.info(f"There are no Uploaded files for {current_card_name}")

                    if files_uploaded >= files_available:
                        self.logger.info(f"Uploaded all available files for {current_card_name}")

                    can_proceed_to_next = self.check_and_click_continue_button()
                    if can_proceed_to_next:
                        return True

            if self.continue_button_clickable():
                self.click_continue_button()
                next_page = self.click_continue_button()
                if next_page:
                    return True
            else:
                self.logger.info("Some Requirements were not met. Cannot proceed to Next Stage.")
                return False
        else:
            self.logger.info("This is not the valid page for this action.")
            return False

    def pass_contact_details(self):
        # Confirm that we are on the vaild page
        if self.on_valid_page('Contact'):
            # Since the information on this page is not really compulsory we can proceed
            progress = self.click_continue_button()
            if progress:
                self.logger.info("All Extra Stage requirements have been filled, Proceeding to next stage...")

            else:
                self.logger.info("Continue button on this page is not clickable.")

        else:
            self.logger.info("This is not the valid page for this action.")

    def pass_extra_stage(self, ni_number):
        # Check to make sure we are on the valid page
        if self.on_valid_page('Extra Information'):
            # Check and send in the NI Number to the required input
            ni_input = self.driver.find_element(By.XPATH,
                                                '//input[@id="MidlandHeartWeb_Theme_wt12_block_OutSystemsUIWeb_wt2_block_wtContent_wtMainContent_wtNINumber_NINumber"]')

            # Checks to see if an NI number has been added to the input field by default
            input_exists = ni_input.get_attribute('value')

            if input_exists.strip():
                self.logger.info("NI Number has been added to input.")
            else:
                self.interact_and_type(ni_input, ni_number)

            progress = self.click_continue_button()
            if progress:
                self.logger.info("All Extra Stage requirements have been filled, Proceeding to next stage...")

        else:
            pass

        # Find the input for the ni number
    def pass_savings_income_stage(self):
        # Confirm that we are on the vaild page
        if self.on_valid_page('savings'):
            # Since the information on this page is not really compulsory we can proceed
            progress = self.click_continue_button()
            if progress:
                self.logger.info("All Extra Stage requirements have been filled, Proceeding to next stage...")

            else:
                self.logger.info("Continue button on this page is not clickable.")

        else:
            self.logger.info("This is not the valid page for this action.")

    def pass_equality_stage(self):
        if self.on_valid_page('Equality'):
            # Since the information on this page is not really compulsory we can proceed
            progress = self.click_continue_button()
            if progress:
                self.logger.info("All Extra Stage requirements have been filled, Proceeding to next stage...")

            else:
                self.logger.info("Continue button on this page is not clickable.")

        else:
            self.logger.info("This is not the valid page for this action.")

    def pass_confirm_details_stage(self):
        if self.on_valid_page('Confirm'):
            # Once we are the valid page we can click on the Yes button to verify
            yes_button = self.driver.find_element(By.XPATH, '//input[@type="radio" and @value="2"]')
            self.interact_and_click(yes_button)

            submit_button = self.driver.find_element(By.XPATH, '//input[@type="submit" and @value="Submit"]')
            self.logger.info("It works, I cannot submit it now...")
            self.interact_and_click(submit_button)

    def start_bot(self):
        """
        Function Starts the bot and makes sure the bot is running
        """
        # Login to the Midland bot website
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")
        self.login_to_website()

        # open the page for all listings in birmingham within a 20 mile radius
        self.logger.info(f"Current Page --> {self.driver.title}")
        self.get_results_for_city()

        # Monitor the listing with the given id and click on the button when the listing becomes available.
        # self.send_message_to_telegram(
        #     f'"Currently Monitoring Listing https://homes.midlandheart.org.uk/Search.PropertyDetails.aspx?PropertyId={self.listing_id}')

        self.logger.info(f"Current Page --> {self.driver.title}")
        self.monitor_listing(self.listing_id)
        time.sleep(3)

        self.pass_eligibility_stage()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_preference_group()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_evidence_stage()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_contact_details()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_extra_stage(self.listing_id)
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_savings_income_stage()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_equality_stage()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")

        self.pass_confirm_details_stage()
        time.sleep(5)
        self.logger.info(f"Current Page --> {self.driver.title}")







