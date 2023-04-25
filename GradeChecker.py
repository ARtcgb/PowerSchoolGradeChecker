import json
import re

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.Properties import Properties
from logger import logger

USERNAME_FIELD_XPATH = '//*[@id="fieldAccount"]'
PASSWORD_FIELD_XPATH = '//*[@id="fieldPassword"]'
LOGIN_BUTTON_XPATH = '//*[@id="btn-enter-sign-in"]'
LAST_UPDATED_XPATH = '//span[@data-ng-if="!!studentAssignmentScoresCtrlData.lastUpdatedDate"]'
SCORE_XPATH = '//*[@id="content-main"]/div[3]/table/tbody/tr[2]/td[5]'
COURSE_NAME_XPATH = '//*[@id="content-main"]/div[3]/table/tbody/tr[2]/td[1]'

SELECT_TARGET = 'score'


class GradeChecker:

    def __init__(self, p_path, j_path):
        self.properties = Properties(p_path).get_properties()
        self.json_file_path = j_path
        self.driver = None

    def setup_driver(self):
        driver_path = Service('chromedriver')
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=driver_path, options=option)
        logger.info("Setting completed")

    def login(self):
        url = self.properties['url']
        user = self.properties['username']
        password = self.properties['password']

        self.driver.get(url)
        self.driver.find_element(By.XPATH, USERNAME_FIELD_XPATH).send_keys(user)
        self.driver.find_element(By.XPATH, PASSWORD_FIELD_XPATH).send_keys(password)
        self.driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()

        WebDriverWait(self.driver, 5, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bold'))
        )
        logger.info("Login succeed")

    def get_course_urls(self):
        url_list = []

        for i in self.driver.find_elements(By.CLASS_NAME, "bold"):
            temp_url = i.get_attribute('href')
            if temp_url is not None and SELECT_TARGET in temp_url:
                url_list.append(temp_url)

        logger.info("Data preprocess completed")
        return url_list

    @staticmethod
    def extract_frn(func_temp_url):
        """
        Extract the frn number from a given URL.

        Args:
            func_temp_url (str): The URL string.

        Returns:
            str: The frn number, or None if not found.
        """
        frn_pattern = r'frn=(\d+)&'
        match = re.search(frn_pattern, func_temp_url)
        if match:
            frn = match.group(1)
            return frn
        else:
            return None

    def extract_score(self, temp_url):
        self.driver.get(temp_url)
        element = self.driver.find_element(By.XPATH, SCORE_XPATH)
        text = element.text.strip()
        score = re.sub(r'\D', '', text)
        return score

    @staticmethod
    def get_last_same_frn_urls(url_list):
        """
        Get the last URL with the same frn number for each group of consecutive URLs with the same frn number.

        Args:
            url_list (list): A list of URLs.

        Returns:
            list: A list of last URLs with the same frn number.
        """
        last_frn = None
        temp_urls = []
        last_same_frn_urls = []

        for func_temp_url in url_list:
            frn = GradeChecker.extract_frn(func_temp_url)
            if frn != last_frn:
                if temp_urls:
                    last_same_frn_urls.append(temp_urls[-1])
                    temp_urls = []
                last_frn = frn
            temp_urls.append(func_temp_url)

        if temp_urls:
            last_same_frn_urls.append(temp_urls[-1])
        logger.info("Data process completed")
        return last_same_frn_urls

    def get_course_data(self, url_list):
        course_data = {}
        for temp_url in url_list:
            self.driver.get(temp_url)
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, LAST_UPDATED_XPATH))
            )
            element = self.driver.find_element(By.XPATH, LAST_UPDATED_XPATH)
            text = element.text.strip().replace("Grades last updated on: ", "")
            course_name = self.driver.find_element(By.XPATH, COURSE_NAME_XPATH).text
            score = self.extract_score(temp_url)
            course_data[course_name] = {'last_updated': text, 'score': score}

        logger.info("Old data extraction completed")
        return course_data

    @staticmethod
    def save_data_to_json(data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def compare_and_load_data_from_json(file_path, new_data):
        try:
            with open(file_path, 'r') as f:
                old_data = json.load(f)
        except FileNotFoundError:
            old_data = {}

        for course_name, new_course_info in new_data.items():
            old_course_info = old_data.get(course_name)
            if old_course_info:
                if old_course_info['last_updated'] != new_course_info['last_updated']:
                    logger.warning(f"{course_name} has a new update: {new_course_info['last_updated']}")
                if old_course_info['score'] != new_course_info['score']:
                    logger.warning(
                        f"{course_name} score changed: {old_course_info['score']} -> {new_course_info['score']}")
        logger.info("Comparison completed")

    def run(self):
        logger.info("Start")
        self.setup_driver()
        self.login()
        url_list = self.get_course_urls()
        url_list = self.get_last_same_frn_urls(url_list)
        course_data = self.get_course_data(url_list)
        self.compare_and_load_data_from_json(self.json_file_path, course_data)
        self.save_data_to_json(course_data, self.json_file_path)
        logger.info("Save & Quit")
