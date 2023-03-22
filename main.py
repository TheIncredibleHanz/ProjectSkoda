# Jan Jiran - task for Škoda Auto - web scraping - 22.03.2023
print("Enviroment Works! Let's scrape! ... for as long as you like!")
## IMPORTS
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import csv
import time

# defining where the data will be stored and what it will look like
filename = 'JiranSkodaZadani.csv' # this should be created automatically within the environment
header = ['datum','cas', 'teplota', 'rychlost_vetru', 'tlak_vzduchu']

# running the open() method on append mode, with a while loop inside to fill the .csv file every 5 minutes
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    # write the header row if the file is empty
    if file.tell() == 0:
        writer.writerow(header)

    while True:
        # Parsing the info using soup
        url = "https://www.fonservis.cz/teplota.php"
        page = requests.get(url)
        # print(page) # 200 if successful
        soup = BeautifulSoup(page.content, 'html.parser')

        spans = soup.find_all('span') # returns blocks called <span> - where time, temperature and wind speed is located (int text)
        bigs = soup.find_all('big') # returns blocks called <big> - in one of them, we can find the air pressure

        # converting to string, so we can use regex
        string1 = str(spans)
        string2 = str(bigs)

        # creating variables to use as data to fill
        aktCas = re.search('(?<=Teplota v Jablonci</a> v )[0-2][0-9]:[0-5][0-9]', string1).group(0) # current time
        aktTeplota = re.search('(?<=Teplota v Jablonci</a> v [0-2][0-9]:[0-5][0-9]: )[0-9]?[0-9]\.[0-9](?=°C)', string1).group(0) # current temperature
        aktVitr = re.search('(?<=Rychlost větru v [0-2][0-9]:[0-5][0-9]: )[0-9]?[0-9]\.[0-9](?= m/s)', string1).group(0) # current wind speed
        aktTlak = re.search('[0-9]?[0-9][0-9][0-9]\.[0-9](?= hPa)', string2).group(0) # current pressure
            # according to regex101.com this:
                # (?<=<font size=\"-1\"><big>Relativní tlak vzduchu: )[0-9]?[0-9][0-9][0-9]\.[0-9](?= hPa)
                # should work for the aktTlak, but it doesn't ... (apparently, there is a problem with the lookbehind statement - nothing seems to fix it):
            # luckily the first value found this way is the correct one, so we can run it without lookbehind

        # there is no date on the web page, but we can use a library to get it
        today = date.today()
        datum = today.strftime("%d/%m/%Y")  # more "Czech" format

        # generate some data to write to the file
        data = [datum, aktCas, aktTeplota, aktVitr, aktTlak]

        # write the data to the file
        writer.writerow(data)

        # wait for 5 minutes (300 seconds) before writing the next data
        time.sleep(300)
