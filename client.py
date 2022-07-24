from http import client
from select import select
from converter import Converter
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class Client(Converter):

    def __init__(self,
                 visit_time, 
                 passport_type,
                 visa_type,
                 passport_number, 
                 name, 
                 surname, 
                 birthday,
                 issue_date, 
                 expiry_date, 
                 issuer, 
                 client_num,
                 webdriver_wait):

        self.visit_time = visit_time
        self.passport_type = passport_type
        self.visa_type = visa_type
        self.passport_number = passport_number
        self.name = name.upper()
        self.surname = surname.upper()
        self.birthday = birthday
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.issuer = issuer
        self.client = str(client_num)
        
        self.wait = webdriver_wait


    def date_conversion(self):
        # This class inherits the Converter class
        # c is the Converter object 
        c = Converter()
        birthday_list = c.convert_date(self.birthday)
        issue_list = c.convert_date(self.issue_date)
        expiry_list = c.convert_date(self.expiry_date)

        # print(birthday_list)
        # print(issue_list)
        # print(expiry_list)

        self.bd, self.bm, self.by = birthday_list 
        self.id, self.im, self.iy = issue_list
        self.ed, self.em, self.ey = expiry_list


    def fill_keys(self):
        passport_number = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="passport_number-{self.client}"]')))
        passport_number.send_keys(self.passport_number)

        first_name = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="first_name-{self.client}"]')))
        first_name.send_keys(self.name)

        last_name = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="last_name-{self.client}"]')))
        last_name.send_keys(self.surname)

        issue_place = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="pptIssuePalace-{self.client}"]')))
        issue_place.send_keys(self.issuer)
        

    def fill_selects(self):
        select_attendance_time = Select(self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="app_time-{self.client}"]'))))
        select_attendance_time.select_by_visible_text(self.visit_time)

        passport = Select(self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="passportType-{self.client}"]'))))
        passport.select_by_visible_text(self.passport_type)

        visa_type = Select(self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="VisaTypeId-{self.client}"]'))))
        visa_type.select_by_visible_text(self.visa_type)
        


    def calculate(self, year, month, day, field):
        birth_click = self.wait.until(EC.element_to_be_clickable((By.XPATH, field))).click()
        calendar_first = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[3]/table/tbody/tr/td/span[1]"))).text
        calendar_last = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[3]/table/tbody/tr/td/span[12]"))).text

        if 'pptExpiryDate' in field:
            while int(calendar_last) < int(year):
                next_switch = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[3]/table/thead/tr/th[3]'))).click()
                calendar_last = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[3]/table/tbody/tr/td/span[12]"))).text
        else:
            while int(calendar_first) > int(year):
                back = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[3]/table/thead/tr/th[1]'))).click()
                calendar_first = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[3]/table/tbody/tr/td/span[1]"))).text

        for var in range(12):
            year_web = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[8]/div[3]/table/tbody/tr/td/span[{var + 1}]")))
            year_str = year_web.text
            if int(year_str) == int(year):
                year_web.click()
                break 

        for var2 in range(12):
            month_web = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[8]/div[2]/table/tbody/tr/td/span[{var2 + 1}]')))
            month_str = month_web.text
            if month_str == month:
                month_web.click()
                break
        
        day_found = False
        for var3 in range(6):
            # print(f'cycle number {var3}')
            if day_found == True:
                break
            else:
                for var4 in range(7):  
                    day_web = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[8]/div[1]/table/tbody/tr[{var3 + 1}]/td[{var4 + 1}]')))
                    day_str = day_web.text                  
                    x = day_web.get_attribute('class')
                    # print(day_str, x, day)
                    if x == 'day' and day_str == str(day):
                        day_web.click()
                        # print('clicked!')
                        day_found = True
                        break
                    else:
                        pass
    
    
    def fill_calendars(self):
        self.date_conversion()
        self.calculate(self.by, self.bm, self.bd, f'//*[@id="date_of_birth-{self.client}"]')

        self.calculate(self.iy, self.im, self.id, f'//*[@id="pptIssueDate-{self.client}"]')
        
        self.calculate(self.ey, self.em, self.ed, f'//*[@id="pptExpiryDate-{self.client}"]')
        
        
