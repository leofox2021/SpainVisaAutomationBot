from cgitb import text
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from converter import Converter

class General(Converter):

    def __init__(self, travel_date, webdriver_wait):
        self.found = False
        self.still_found = False
        self.travel_date = travel_date

        self.wait = webdriver_wait
    

    def date_conversion(self, date):
        c = Converter()
        travel_list = c.convert_date(self.travel_date)

        self.td, self.tm, self.ty = travel_list 


    def find_booking_day(self):

        for var in range(6):
            for var2 in range(7): 
                day_web = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[8]/div[1]/table/tbody/tr[{var + 1}]/td[{var2 + 1}]')))
                x = day_web.get_attribute('title')
                # print(x)
                if x == 'Book':
                    day_web.click()
                    self.found = True
                    break
                else:
                    pass
    

    def still_find_booking_month(self):
            if self.found == False:
                month_select = self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/table/thead/tr[1]/th[2]'))).click()
                for var3 in range(12):
                    month_str = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[8]/div[2]/table/tbody/tr/td/span[{var3 + 1}]')))
                    y = month_str.get_attribute('class')
                    if y == 'month active':
                        month_str.click()
                        still_found = True
                        self.find_booking_day()
                        break
                    else: 
                        pass
            else: 
                pass


    def find_travel_day(self, day):
        day_found = False
        for var in range(6):
            if day_found == True:
                break
            else:
                for var2 in range(7):  
                    day_web = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[8]/div[1]/table/tbody/tr[{var + 1}]/td[{var2 + 1}]')))
                    day_str = day_web.text     
                    # print(day_str)              
                    x = day_web.get_attribute('class')
                    if x == 'day' and day_str == str(day):
                        day_web.click()
                        # print('clicked!')
                        day_found = True
                        break
                    else:
                        pass


    def find_travel_month(self, month):
        for var2 in range(12):
            month_web = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[8]/div[2]/table/tbody/tr/td/span[{var2 + 1}]')))
            month_str = month_web.text
            m = month_web.get_attribute('class')
            if m == 'month':
                if month_str == month:
                    month_web.click()
                    break
            else:
                pass
    

    def find_travel_year(self, year):
        for var in range(12):
            year_web = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[8]/div[3]/table/tbody/tr/td/span[{var + 1}]")))
            year_str = year_web.text
            y = year_web.get_attribute('class')
            if y == 'year':
                if int(year_str) == int(year):
                    year_web.click()
                    break 

    
    def pick_booking_date(self):
        visit_day = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app_date"]'))).click()
        self.find_booking_day()
        if self.found == False:
            self.still_find_booking_month()
        return self.found


    def pick_travel_date(self):
        travel_date_click = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="travelDate"]'))).click()
        self.date_conversion(self.travel_date)
        calendar_header = self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/table/thead/tr[1]/th[2]')))
        text_header = calendar_header.text
        if self.tm in text_header:
            print('1')
            self.find_travel_day(self.td)
        else:
            print('2')
            while self.tm not in text_header:
                next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[1]/table/thead/tr[1]/th[3]'))).click()
                calendar_header = self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/table/thead/tr[1]/th[2]')))
                text_header = calendar_header.text

            if self.ty in text_header:
                print('2.5')
                self.find_travel_day(self.td)
            else:
                print('3') 
                self.find_travel_year(self.ty)
                self.find_travel_month(self.tm)
                self.find_travel_day(self.td)

