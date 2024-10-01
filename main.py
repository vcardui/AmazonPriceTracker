import smtplib
import requests
from bs4 import BeautifulSoup

# Email data
my_email = "carduibot@gmail.com"
password = "ydffosgveywfvfrr"

# Amazon link and headers
URL = ("https://www.amazon.com.mx/Complete-Asimovs-Foundation-Foundations-Prelude/dp/B01EFDEMS8/ref=sr_1_2?crid"
       "=NGK2HFJBXUQ&dib=eyJ2IjoiMSJ9.nLMvMxRE3144e3lyUWZmRdu3StUyZeqOR2ah"
       "-g8LeXPZa_S9MINoQX8UNUCWrOpifrD5RLkhZs5u5LldH9hHreIbNOY9_c6dKfXbXdHSriqqLoJ8COUAudtYdVPU6aIWmbtSuViebER5FjSbO01NadDGYBOL7OczSa-wnQqBuJEQ1uVJSnS8Xmh_qb_n0eVfZHrb3PqUoA28tifjvTEMUGNS43bvRfNlfSN0jRvdC-M.Fq7QSAOKRH_7nBlCa1X1ANhbKOO5bW5_ziaSldC7CpQ&dib_tag=se&keywords=foundation+isaac+asimov&qid=1709418725&s=books&sprefix=the+found%2Cstripbooks%2C123&sr=1-2&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47")

AMZN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.3.1 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9"
}

# Get the product's price
response = requests.get(URL, headers=AMZN_HEADERS)
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')
price_today = float(soup.find_all(name="span", class_="a-size-medium a-color-price header-price a-text-normal")[
    0].getText().replace('$', ''))

# print(soup)
print(f"Today's price: ${price_today}")

# Getting the lowest price on record
with open(f"lowestPrice.txt", 'r') as lowestPrice_file:
    lowest_record_price = float(lowestPrice_file.read())

# Send myself an email if price is below the record
if price_today < lowest_record_price:
    email_body = (f"Hello there! CarduiBot here,"
                  f"\n\nThe Complete Isaac Asimov's Foundation Series Books 1-7 current price is ${price_today}"
                  f"\n\tLowest previous price: ${lowest_record_price}"
                  f"\n\tSavings: ${lowest_record_price - price_today}"
                  "\nBuy it now! :D"
                  f"\nLink to product: {URL}"
                  "\n\nBest regards,"
                  "\nCarduiBot")
    print(email_body)

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs="vanessa@reteguin.com",
                        msg=f"Subject: Discount on Amazon!\n\n{email_body}")
    connection.close()
    print("Email Sent successfully")

    with open("lowestPrice.txt", mode="w") as file:
        file.write(f"{price_today}")

    print("lowestPrice.txt overwritten successfully")