# +----------------------------------------------------------------------------+
# | CARDUI TECH v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2026 - 2026, CARDUITECH.COM (www.carduitech.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.carduitech.com/license/
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | First release: March 2nd, 2024
# | Last update..: March 18th, 2026
# | WhatIs.......: Amazon Price Tracker (Web Scrapping exercise)  - Main
# +----------------------------------------------------------------------------++

# ------------ Resources / Documentation involved -------------

# -------------------------- Imports --------------------------
from DataSearcher_class import DataSearcher


# ------------------------- Libraries -------------------------
import re # regular expressions
import datetime  # datetime.datetime.now()
import pandas as pd

# Send emails imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ------------------------- Variables -------------------------
# Time
now = datetime.datetime.now()
todayDate = now.strftime("%d/%m/%Y")
todayTime = now.strftime("%H:%M")

emailSubject = f"This is a test {todayDate} at {todayTime}"

# Email data
botEmail = ""
botPassword = ""

myEmail = ""


# Records files
records_Folder = 'records'
HairCurler_FileName = 'HairCurler_PriceTracker.csv'
records_Path = f'{records_Folder}/{HairCurler_FileName}'

# Product link and headers
URL_AMAZON = ("https://www.amazon.com.mx/TYMO-CurlPro-Plus-automático-antiarañazos/dp/B0DPZLWX8J/ref=sr_1_5?dib=eyJ2IjoiMSJ9.ld0u-T3tBmFTSNQUWDBq31yxQ95QJjt1jTLeXqFB0HAy223q_CrNGADpB2-l5CA2lPPFE-X0zjLBs36sp3PkazpA94db9Re4fY0DPb--jk9E5hKWbRD0Q0_1vJqNDyRq8lET4CrgdVOAKAkHWzhles_BfmfJk8dHQxfoY1iCNLZMP8PXFUHzCQvRmLlyBgIDbn30mGPUWMDUvqTS9EJWrEuI6ZfFLC6dalt8K8NROaW3BWUvZaPXQ4Cz7hcyw6i6E5SRp6RrtbJ_70B9rkaf8cTwhwTaUXvVfgI6qxX7fh4.vUC0Q7AcoidaHgR-JTUNstrAlBaRHXlcJ37CTiEKT2o&dib_tag=se&keywords=TYMO%2BCURLPRO%2BPLUS&qid=1773695407&sr=8-5&ufe=app_do%3Aamzn1.fos.de93fa6a-174c-4df7-be7c-5bc8e9c5a71b&th=1")
HEADERS_AMAZON = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "CCBot/2.0 (https://commoncrawl.org/faq/)"
}

URL_TYMO = ("https://tymobeauty.com/products/tymo-curlpro-plus")
HEADERS_TYMO = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "CCBot/2.0 (https://commoncrawl.org/faq/)"
}

# --------------------------- Code ----------------------------
webData_amazon = DataSearcher(url=URL_AMAZON, headers = HEADERS_AMAZON)
price_amazon = webData_amazon.get_data(tag_name="span", tag_class="a-price-whole", show_value=False)
price_amazon = float(re.sub(r'[,\n\r ]', '', price_amazon))
print(f"Price Amazon: ${price_amazon} MXN")

webData_tymo = DataSearcher(url=URL_TYMO, headers = HEADERS_TYMO)
price_tymo = webData_tymo.get_data(tag_name="span", tag_class="money", show_value=False)
price_tymo = float(re.sub(r'[,$\n\r ]', '', price_tymo))
print(f"Price Tymo: ${price_tymo} MXN")

new_records = {
    "datetime": [pd.Timestamp.now(), pd.Timestamp.now()],
    "provider": ["Amazon", "Tymo"],
    "price": [price_amazon, price_tymo]
}

records_Dataframe = []
new_rows = pd.DataFrame(new_records)

try:
    records_Dataframe = pd.read_csv(records_Path)
    records_Dataframe = pd.concat([records_Dataframe, new_rows], ignore_index=True)
    records_Dataframe.to_csv(records_Path, index=False)
    print("File's data successfully updated")

except FileNotFoundError or IndexError:
    print(f'File not found. Creating CSV at {records_Folder}')
    records_Dataframe = pd.DataFrame(new_records)
    records_Dataframe.to_csv(records_Path, index=False)
    print("File successfully created")


allTime_lowestPrice = records_Dataframe.loc[records_Dataframe['price'].idxmin()]
print(f"\nAll time Lowest Price:\n{allTime_lowestPrice}")

today_lowestPrice = new_rows.loc[new_rows['price'].idxmin()]
print(f"\nToday Lowest Price:\n{today_lowestPrice}")

if today_lowestPrice['price'] < allTime_lowestPrice['price']:
    conclusion = 'This is a record! <span class="good">You should buy</span> your product today'
    print(f"\nThis is a record, ${today_lowestPrice['price']}! You should buy your product today")
else:
    conclusion = 'Today is <span class="bad">not a good</span> day to buy your product'
    print(f"\nYour product's price today is: ${today_lowestPrice['price']}\nDifference against record low price (${allTime_lowestPrice['price']}) is: ${today_lowestPrice['price'] - allTime_lowestPrice['price']}")

email_body = f'''
<html>
    <head>
        <style>
            .amazon {{
                color: #FF9900;
                font-weight: bold;
                text-decoration: none;
            }}
            .tymo {{
                color: #AC2A45;
                font-weight: bold;
                text-decoration: none;
            }}
            .good {{
                color: #32CD32;
                font-weight: bold;
            }}
            .bad {{
                color: #FF7034;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>TYMO Curl Pro Plus</h1>
        <h2>Today prices</h2>
        <p>Price <a href="{URL_AMAZON}" class="amazon" target="_blank">Amazon</a>: ${price_amazon} MXN</p>
        <p>Price <a href="{URL_TYMO}" class="tymo" target="_blank">Tymo</a>: ${price_tymo} MXN</p>
        <h2>Record</h2>
        <p><b>All time Lowest Price:</b> ${allTime_lowestPrice['price']} ({allTime_lowestPrice['provider']} - {allTime_lowestPrice['datetime']})</p>
        <p><b>Today Lowest Price:</b> ${today_lowestPrice['price']} ({today_lowestPrice['provider']} - {today_lowestPrice['datetime']})</p>
        <p>Difference against record low price (${allTime_lowestPrice['price']}) is: ${today_lowestPrice['price'] - allTime_lowestPrice['price']}</p>
        <h2>Conclusion</h2>
        <p>{conclusion}</p>
    </body>
</html>
'''
print(email_body)

# Create email message container
email = MIMEMultipart('alternative')
email['Subject'] = emailSubject
email['From'] = botEmail
email['To'] = myEmail

# Record the MIME type email's HTML part
HTMLPart = MIMEText(email_body, 'html')

email.attach(HTMLPart)

print(email.as_string())

# Send message with smtplib

connection = smtplib.SMTP("smtp.gmail.com",
                          587)  # port 587, which is specifically configured for secure email transmission
connection.starttls()  # Secure connection
connection.login(user=botEmail, password=botPassword)
connection.sendmail(from_addr=botEmail,
                    to_addrs=myEmail,
                    msg=email.as_string())
connection.close()
print("Email Sent successfully")