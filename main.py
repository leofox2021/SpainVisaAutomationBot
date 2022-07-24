import os, sys, time, datetime, imaplib, email
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from openpyxl import load_workbook
from twocaptcha import TwoCaptcha
from client import Client #Imported from client.py
from general import General #Imported from general.py
from converter import Converter #Imported from converter.py
from verification import get_verification_code


class MyChrome(uc.Chrome):
    def __del__(self):
        pass


def load_from_excel(driver):
    register_fail = False
    all_customers.clear()

    try:
        book = load_workbook('USER_DATA.xlsx')
    except Exception as ex:
        # os.system('cls' if os.name == 'nt' else 'clear')
        print(ex)
        print('Не удалось загрузить таблицу USER_DATA.')
        print('Если вы нарушили целостность таблицы, пожалуйста переустановите программу.')
        driver.close()
        # reportError('Не удалось загрузить таблицу USER_DATA. \nЕсли вы нарушили целостность таблицы, пожалуйста переустановите программу.')
        register_fail = True
        return register_fail
    else:
        sheet = book.active
        rows = sheet.rows
        ended = False
        

        while ended == False:
            try: 
                items = [cell.value for cell in next(rows)]
            except Exception:
                ended = True
            else:
                if len(all_customers) == 8:
                    pass
                else:
                    if items[0] == None:
                        pass
                    else:
                        all_customers.append(items)
            
        all_customers.pop(0)
        global x
        x = len(all_customers)


def toLogTxt(message, ex):
    with open('log.txt', 'w', encoding='utf-8') as log_txt:
        log_txt.write(message, '\n')
    print(ex)
    print(message)


with open('context/members.txt', 'r+', encoding='utf-8') as members:
    m1 = members.read()
    m2 = m1.replace('\ufeff', '')
    m3 = m2.replace('\n', '')


with open('context/visa_center.txt', 'r+', encoding='utf-8') as center:
    c1 = center.read()
    c2 = c1.replace('\ufeff', '')
    c3 = c2.replace('\n', '')


with open('context/phone.txt', 'r+', encoding='utf-8') as phone:
    p1 = phone.read()
    p2 = p1.replace('\ufeff', '')
    p3 = p2.replace('\n', '')


with open('context/email.txt', 'r+', encoding='utf-8') as email:
    e1 = email.read()
    e2 = e1.replace('\ufeff', '')
    e3 = e2.replace('\n', '')


with open('context/password.txt', 'r+', encoding='utf-8') as password_txt:
    ps1 = password_txt.read()
    ps2 = ps1.replace('\ufeff', '')
    ps3 = ps2.replace('\n', '')


with open('context/travel_date.txt', 'r+', encoding='utf-8') as travel_date:
    t1 = travel_date.read()
    t2 = t1.replace('\ufeff', '')
    t3 = t2.replace('\n', '')


# VARIABLES
# URL = 'file:///C:/Users/user/Downloads/blsspain-russia.com.html'
# HCAPTCHA = f'file:///{os.getcwd()}/html/hcaptcha.html'
URL = 'https://blsspain-russia.com/moscow/book_appointment.php'
captcha_config = {
            'server':           '2captcha.com',
            'apiKey':           'b9b46febb9203a26d03df1f13b4dc76d',
            'callback':         'https://your.site/result-receiver',
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10
        }
solver = TwoCaptcha(**captcha_config)
d = MyChrome(use_subprocess=True)
wait = WebDriverWait(d, 90)
all_customers = []
g = General(t3, wait)
# Logging n first time crashes the fill page
# Вход в прервый раз возвращает обратно на страницу входа
d.get(URL) 
time.sleep(1)
# Log in once more to finally get to the fill page
# Вход еще раз, чтобы попасть на страницу заполнения
d.get(URL) 


# PAGE 1

def login_page():
    try:
        el1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app_type2"]'))).click()
        members = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="member"]')))).select_by_visible_text(f'{m3} Members')
        visa_center = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="centre"]')))).select_by_index(1)
        phone = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="phone"]'))).send_keys(p3)
        email = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="email"]'))).send_keys(e3)
        visa_type = Select(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]'))))
        visa_type.select_by_index(1)
        request_code = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/section[1]/div/div/div[2]/div[2]/div[7]/div[2]/abbr/a'))).click()
        time.sleep(2)
        print(e3)
        print(ps3)
        code = get_verification_code(e3, ps3, "imap.yandex.com")
        # print(code)
        code_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="otp"]'))).send_keys(code)
        proceed = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/section[1]/div/div/div[2]/div[2]/div[8]/div[3]/input'))).click()
    except Exception as ex:
        message1 = 'Ошибка сайта, или данные из папки context заполнены неправильно'
        toLogTxt(message1, ex)
        d.close()
        sys.exit()
    else:
        # PAGE 2
        confirm = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Booking"]/section/div/div/div/div[8]/div[1]/button'))).click()


login_page()
login_page()
# print(d.current_url)
# fillcaptcha(solver, 'https://blsspain-russia.com/moscow/appointment_family.php', wait)

# PAGE 3
booking_date = g.pick_booking_date()
if booking_date == False:
    message4 = "На данный момент нет свободных мест."
    toLogTxt(message4, ex)
    d.close()
    sys.exit()
else:
    pass


# sitekey = "748d19a1-f537-4b8b-baef-281f70714f56"
# captcha_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="captcha"]'))).send_keys('remuiisa')
# email2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))).send_keys('testingemail@gmail.com')
# phone2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="phone"]'))).send_keys(p3)
request_otp = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ap_tr"]/td[2]/abbr/a'))).click()
try:
    g.pick_travel_date()
except Exception as ex2:
    message2 = 'Ошибка. Проверьте правильность введенных данных в "context/travel_date"'
    toLogTxt(message2, ex2)
    d.close()
else:
    pass

load_from_excel(d)
for var3 in all_customers:
    print(var3)

for var in range(x):
    try:
        c = Client(all_customers[var][0],
                    all_customers[var][1],
                    all_customers[var][2], 
                    all_customers[var][3],
                    all_customers[var][4],
                    all_customers[var][5],
                    all_customers[var][6],
                    all_customers[var][7],
                    all_customers[var][8],
                    all_customers[var][9],
                    var + 1, 
                    wait)
        
        c.fill_selects()
        c.fill_keys()
        c.fill_calendars()
    except Exception as ex3:
        message3 = 'Ошибка. Проверьте правильность введенных данных в таблице USER_DATA.'
        toLogTxt(message3, ex3)
        d.close()
    else: 
        pass

# captcha_code = fillcaptcha()

