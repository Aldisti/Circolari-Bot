from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time



def factorization(n):
    driver.get("https://www.alpertron.com.ar/ECM.HTM") # apro Alpertron
    input = driver.find_element_by_xpath('//*[@id="value"]') # seleziono la casella dove inserire il numero da fattorizzare
    try:
        driver.find_element_by_xpath('//*[@id="stop"]').click() # fermo la fattorizzazione
    except:
        pass
    input.clear() # pulisco la casella di input
    input.send_keys(str(n))
    driver.find_element_by_xpath('//*[@id="factor"]').click()
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/ul[1]/li')))
        return driver.find_element_by_xpath('//*[@id="result"]/ul[1]/li').text.split()
    except:
        pass
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="status"]')))
        timeToEnd = driver.find_element_by_xpath('//*[@id="status"]').text.split()[driver.find_element_by_xpath('//*[@id="status"]').text.split().index('End')+3:]
        if timeToEnd[0][:-1] != '0' or timeToEnd[1][:-1] != '0' or int(timeToEnd[2][:-1]) > 2:
            return 1
        else:
            wait = WebDriverWait(driver, (int(timeToEnd[2][:-1]) * 60 + int(timeToEnd[3][:-1]) + 10))
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/ul[1]/li')))
                return driver.find_element_by_xpath('//*[@id="result"]/ul[1]/li').text.split()
            except:
                try:
                    return driver.find_element_by_xpath('//*[@id="result"]/p[1]').text.split()
                except:
                    return 1
    except:
        wait = WebDriverWait(driver, 30)
        try:
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="result"]/p[1]'), '×'))
            return driver.find_element_by_xpath('//*[@id="result"]/p[1]').text.split()
        except:
            try:
                return driver.find_element_by_xpath('//*[@id="result"]/p[1]').text.split()
            except:
                return 1

def StartFactorization(number):
    global driver
    driver = webdriver.Chrome(executable_path="C:\\Users\\aless\\Downloads\\chromedriver.exe")

    alfa = {'FF': 0, 'CF': 0, 'C': 0, 'Time': float(time.time())}
    cont = 0

    for _ in range(number):
        driver.get("http://factordb.com/") # apro il sito di Factordb
        status = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[5]/a') # cerco il link status
        status.click() # clicco il link status
        element = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[5]/td[1]/a') # cerco il link dei numeri con fattori sconosciuti (C)
        element.click() # clicco il link C
        startInput = driver.find_element_by_name('start') # cerco la casella per impostare i numeri da saltare (start)
        startInput.clear() # elimino tutte le scritte dalla casella
        startInput.send_keys('50') # inserisco il valore
        showButton = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[7]/td/input') # cerco il pulsante show
        showButton.click() # premo il pulsante show
        driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/a[2]/font').click() # prendo il primo numero della lista
        number = driver.find_element_by_xpath('/html/body/form[1]/center/input[1]') # seleziono la casella dove è contenuto il numero
        n = number.get_property('value') # estraggo il numero dalla casella
        result = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]').text # prendo il valore dello status del numero

        if result == 'C': # controllo che il numero non sia ancora stato fattorizzato
            factorsraw = factorization(n) # fattorizzo il numero
            if factorsraw != 1:
                try:
                    factors = [i[:i.index('(')] if 'digits' in i else i for i in "".join(factorsraw[factorsraw.index('=')+1:]).split('×')]
                    driver.get("http://factordb.com/") # apro di nuovo Factordb
                    input = driver.find_element_by_xpath('/html/body/form/center/input[1]') # seleziono la casella dove inserire il numero da cercare
                    input.clear() # cancello tutti i caratteri presenti nella casella
                    input.send_keys(str(n), Keys.ENTER) # cerco il numero fattorizato
                    if driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]').text != 'FF':
                        reportInput = driver.find_element_by_xpath('/html/body/form[2]/center/table/tbody/tr[2]/td/textarea') # seleziono la casella dove inserire i fattori
                        for i in factors:
                            reportInput.send_keys(str(i), Keys.ENTER) # inserisco tutti i fattori
                        driver.find_element_by_xpath('/html/body/form[2]/center/table/tbody/tr[4]/td/input').click() # clicco il pulsante per reportare i fattori
                        cont += 1
                        alfa[driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[3]/td[1]').text] += 1
                except:
                    pass
    alfa['Time'] = str((float(time.time()) - alfa['Time']) / 60) + ' minutes' if ((float(time.time()) - alfa['Time'])) / 60 < 60 else str(((float(time.time()) - alfa['Time']) / 60) / 60) + ' hours'
    return alfa

print(StartFactorization(15))
