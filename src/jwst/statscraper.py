from decimal import *
from distutils.util import strtobool
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options

def toCelcius(temp):
    try:
        return (temp - 32) * 5 / 9
    except Exception as e:
        print(str(e))
        return temp

def milestoKm(miles):
    try:
        conv_factor = Decimal(1.60934)
        return Decimal(miles) * conv_factor
    except Exception as e:
        print(str(e))
        return miles

class StatScraper:

    driver = None

    STATS_PAGE = 'https://www.jwst.nasa.gov/content/webbLaunch/whereIsWebb.html'

    def __init__(self, config: dict) -> None:
        self.config = config
        self.init_driver()

    def init_driver(self) -> None:
        chrome_options = Options()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage') # fixes crash in docker
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')

        chrome_prefs = {}
        chrome_prefs['profile.default_content_settings'] = {'images': 2}
        chrome_options.experimental_options['prefs'] = chrome_prefs

        if strtobool(self.config.get('USE_LOCAL_DRIVER')):
            self.driver = webdriver.Chrome(options=chrome_options, executable_path=self.config.get('LOCAL_DRIVER_PATH'))
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def open_stat_page(self) -> None:
        print("Opening stats page...")
        self.driver.get(self.STATS_PAGE)
        wait = ui.WebDriverWait(self.driver, 6)
        wait.until(lambda driver: driver.find_element_by_id('milesEarth').text != 0)

    def get_stats(self) -> dict:
        print("Getting stats...")

        # open the page if it isn't already open
        if self.driver.current_url != self.STATS_PAGE:
            self.open_stat_page()

        milesFromEarth = self.driver.find_element_by_id('milesEarth').text
        milesToL2 = self.driver.find_element_by_id('milesToL2').text
        percentageCompleted = self.driver.find_element_by_id('percentageCompleted').text
        cruisingSpeed = self.driver.find_element_by_id('speedMi').text
        tempWarmSide1F = self.driver.find_element_by_id('tempWarmSide1F').text
        tempWarmSide2F = self.driver.find_element_by_id('tempWarmSide2F').text
        tempCoolSide1F = self.driver.find_element_by_id('tempCoolSide1F').text
        tempCoolSide2F = self.driver.find_element_by_id('tempCoolSide2F').text

        return {
                'distanceFromEarth': {
                    'miles': Decimal(milesFromEarth),
                    'km': milestoKm(milesFromEarth)
                },
                'distanceToL2': {
                    'miles': Decimal(milesToL2),
                    'km': milestoKm(milesToL2)
                },
                'percentageCompleted': percentageCompleted,
                'cruisingSpeed': {
                    'miles': Decimal(cruisingSpeed),
                    'km': milestoKm(cruisingSpeed)
                },
                'tempWarmSide1': {
                    'F': tempWarmSide1F,
                    'C': toCelcius(tempWarmSide1F)
                },
                'tempWarmSide2': {
                    'F': tempWarmSide2F,
                    'C': toCelcius(tempWarmSide2F)
                },
                'tempCoolSide1': {
                    'F': tempCoolSide1F,
                    'C': toCelcius(tempCoolSide1F)
                },
                'tempCoolSide2': {
                    'F': tempCoolSide2F,
                    'C': toCelcius(tempCoolSide2F)
                }
        }        