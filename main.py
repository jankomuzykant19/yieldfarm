from selenium import webdriver
from requests import get
import csv
import time

URL = 'https://etherscan.io/yieldfarms'


class scraper():
    def __init__(self):
        self.driver = webdriver.Chrome('/Users/jasiek/PycharmProjects/yieldfarm/chromedriver')
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)

    def get_data(self):
        self.driver.get(URL)
        time.sleep(3)

        # AMOUNT OF PAGES
        amount_of_pages = int(self.driver.find_element_by_xpath('//span[@class="paginate_total"]').text)
        next_page_button = self.driver.find_element_by_xpath('//*[@id="mytable_next"]/a')
        for page in range(amount_of_pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # PROJECT NAMES
            project_names = []
            projects = self.driver.find_elements_by_xpath(
                '//div[@class="media align-items-center"]')
            for project in projects:
                if 'Sponsored' in project.text:
                    project_names.append(project.text.replace('\nSponsored', ''))
                elif project.text == '':
                    pass
                else:
                    project_names.append(project.text)

            # print(project_names)
            # print(len(project_names))

            # SYMBOLS
            symbols_list = []
            symbols = self.driver.find_elements_by_xpath('//a[@class="text-primary"]')
            for symbol in symbols:
                if symbol.text == "":
                    pass
                else:
                    symbols_list.append(symbol.text)

            # print(symbols_list)
            # print(len(symbols_list))

            # WEBSITE
            websites_list = []
            websites = self.driver.find_elements_by_xpath('//a[@rel="nofollow noopener"]')
            for website in websites:
                if '.' in website.text:
                    websites_list.append(website.text)

            # print(websites_list)
            # print(len(websites_list))

            # TOKEN ADDRESSES
            tokens_list = []
            tokens = self.driver.find_elements_by_xpath('//a[@class="hash-tag text-truncate"]')
            for token in tokens:
                if token.text != '':
                    tokens_list.append(token.text)

            # print(tokens_list)
            # print(len(tokens_list))

            # DATE START
            dates_list = []
            dates = self.driver.find_elements_by_xpath('//td[@class="sorting_3"]')
            for date in dates:
                if date.text != '':
                    dates_list.append(date.text)

            # print(dates_list)
            # print(len(dates_list))

            # PRICE
            prices_list = []
            for x in range(1, len(project_names) + 1):
                price = self.driver.find_element_by_xpath('//*[@id="mytable"]/tbody/tr[' + str(x) + ']/td[6]')
                prices_list.append(price.text)

            # print(prices_list)
            # print(len(prices_list))

            # MARKET CAP
            caps_list = []
            for x in range(1, len(project_names) + 1):
                cap = self.driver.find_element_by_xpath('//*[@id="mytable"]/tbody/tr[' + str(x) + ']/td[7]')
                caps_list.append(cap.text)

            # print(caps_list)
            # print(len(caps_list))

            # DYOR
            dyors_list = []
            for x in range(1, len(project_names) + 1):
                dyor = self.driver.find_element_by_xpath('//*[@id="mytable"]/tbody/tr[' + str(x) + ']/td[8]')
                dyors_list.append(dyor.text)

            # SAVING TO CSV
            f = open("yieldfarm.csv", "a", newline="")
            for x in range(len(project_names)):
                tup = (
                project_names[x], symbols_list[x], websites_list[x], tokens_list[x], dates_list[x], prices_list[x],
                caps_list[x], dyors_list[x])
                writer = csv.writer(f)
                writer.writerow(tup)
            f.close()

            # NEXT PAGE
            print(f"Working on page: {page + 1}")
            if (page < amount_of_pages - 1):
                next_page_button.click()


def main():
    scraper1 = scraper()
    scraper1.get_data()


main()
