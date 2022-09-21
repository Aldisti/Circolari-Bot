from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from os import listdir, remove
from pyrogram import Client
from sqlite3 import connect
import requests
import PyPDF2



RESULTS = {
    'comunicazioni': 0,
    'circolari': 0,
    'link': 0,
    'file': 0,
    'pdf': 0,
    'testo': 0,
    'foto': 0,
    'esaminato': 0,
    'inviato': 0,
    'eliminato': 0,
    'PermissionError': 0,
    'FileNotFoundError': 0
}

CREDENZIALI = {
    "codice": "ss16749",
    "username": "ale-diste_04.",
    "password": "milva63"
}

KEYWORDS = {
        "5s": 0.5,
        "5^s": 0.5,
        "5 s": 0.5,
        "assemblea d'istituto": 1,
        "assemblea sindacale": 1,
        "classi quinte": 0.5,
        "classe quinta": 0.5,
        "sciopero": 0.25,
        "entrata posticipata": 1
}

URL = "https://lordeummfo.tappo03.it/pdf/5vlAAqp90knELhBgdDhN"


options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\aless\Downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
options.add_argument('--kiosk-printing')
options.add_argument('--incognito')
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument("--disable-plugins-discovery")

APP = Client(
    "B0BB0BOT",
    api_id = 7775230,
    api_hash = "9969d92d115b3941a78ef9001aefdf50",
    bot_token = "2089459247:AAG0UVBUr3Vdf8syrjg413gUJH4KPsdQjfM")

def checkio(path):
    # file analyzer
    pdfReader = PyPDF2.PdfFileReader(rf"C:\Users\aless\Downloads\{path}")
    cont, pages, er = 0, pdfReader.numPages, 0
    text = ''
    for i in range(pages):
        try:
            page_text = pdfReader.getPage(i).extractText().strip().replace('\n', '')
        except Exception as e:
            er += 1
            print('\n', e, '\n', er, '\n')
        cont += 1 if len(page_text) > 334 else 0
        text += page_text.lower()

    if cont == 0 and pages <= 4:
        RESULTS['foto'] += 1
        RESULTS['testo'] -= 1
        files = [('file',('Why_do_you_need_my_name?', open(rf"C:\Users\aless\Downloads\{path}", 'rb'), 'application/pdf'))]
        response = requests.request("POST", URL, files=files)
        text = response.text[23:-1].lower()
        files[0][1][1].close()
    cont = 0
    for key in KEYWORDS:
        cont += text.count(key) * KEYWORDS[key]
    RESULTS['esaminato'] += 1

    return cont >= 1



d = webdriver.Chrome(executable_path = "C:\\Users\\aless\\Downloads\\chromedriver.exe", options = options)
wait = WebDriverWait(d, 10)

d.get("https://www.portaleargo.it/argoweb/famiglia/index.jsf#")

wait.until(EC.presence_of_element_located((By.ID, "codiceScuola")))

d.find_element(By.ID, "codiceScuola").send_keys(CREDENZIALI["codice"])
d.find_element(By.ID, "username").send_keys(CREDENZIALI["username"])
d.find_element(By.ID, "password").send_keys(CREDENZIALI["password"])

d.find_element(By.ID, "accediBtn").click()

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_idJsp27"]/div[1]')))
d.find_element(By.XPATH, '//*[@id="_idJsp27"]/div[1]').click()
d.find_element(By.XPATH, '//*[@id="bacheca"]/table/tbody/tr[3]/td[2]/div/div[3]').click()
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sheet-bacheca:tree:scuola"]/div/span/label')))
d.find_element(By.XPATH, '//*[@id="sheet-bacheca:tree:scuola"]/div/span/label').click()

wait.until(EC.presence_of_element_located((By.TAG_NAME, 'fieldset')))
container = d.find_elements(By.TAG_NAME, 'fieldset')

con = connect(r"C:\Users\aless\OneDrive\Python\Circolari\Database.db")
cur = con.cursor()

for element in container:
    RESULTS['comunicazioni'] += 1
    if 'File' in element.text:
        RESULTS['circolari'] += 1
        for link_text in [i.split(':')[1].strip() for i in element.text.split('\n') if 'File' in i]:
                RESULTS['link'] += 1
                DOWNLOADS = listdir(r"C:\Users\aless\Downloads")
                d.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))))

                def checkD():
                    while True:
                        for i in list(set(listdir(r"C:\Users\aless\Downloads")) - set(DOWNLOADS)):
                            if 'tmp' not in i and 'crdownload' not in i:
                                    return
                checkD()

                file_name = list(set(listdir(r"C:\Users\aless\Downloads")) - set(DOWNLOADS))[0]

                RESULTS['file'] += 1
                temp = cur.execute("SELECT name FROM circolari")
                con.commit()
                db_files = [str(i[0]) for i in temp]
                del temp

                if file_name.endswith('.pdf') and file_name not in db_files:
                    RESULTS['pdf'] += 1
                    RESULTS['testo'] += 1
                    if checkio(file_name):
                        RESULTS['inviato'] += 1
                        with APP:
                            APP.send_message('Aldisti0', f"Ciao, potrebbe interessarti questa circolare!")
                            APP.send_document('Aldisti0', rf"C:\Users\aless\Downloads\{file_name}")
                    cur.execute("""INSERT INTO circolari VALUES (?, ?);""", (None, file_name))
                    con.commit()

                remove(rf"C:\Users\aless\Downloads\{file_name}")
                RESULTS['eliminato'] += 1
                print(RESULTS)

con.commit()
con.close()
