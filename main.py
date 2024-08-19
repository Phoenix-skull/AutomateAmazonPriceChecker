import smtplib
import os
from itertools import product

from charset_normalizer.api import explain_handler
from dotenv import load_dotenv
import bs4
import requests


load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("APP_PASSWORD")

URL = "https://www.amazon.com/Razer-DeathAdder-HyperSpeed-Wireless-Esports/dp/B0D4RF55QK/ref=sr_1_2?crid=3DAXWFEMSGABR&dib=eyJ2IjoiMSJ9.aLHnjMRQudQlZmBfphsP-eLjq4UKhtBWypBxclX-HY6B51FQOr4yeDFDaZImNDuyM5UJgxx6SIWV7tiPWm3ergDKniLlzEyuMtwPHGA8kyF8HSeXK6tkriYDzJ6hv_OW_FTP06DtMhf8oticARLPrTEqkCaGdOAQAAgid1Ibn75OwQX3ypffzwUroYTyCS9-vP4C7Le7_kqDPMDEJD9lMxR41-IAreO0RDGJL6SRoXg.tw4-8q2FQf3lM1-Uv_ctkdrqsTtmSufzrhnP-ZAF_fE&dib_tag=se&keywords=Razer+DeathAdder+V3+HyperSpeed&qid=1724057946&sprefix=razer+deathadder+v3+hyperspeed%2Caps%2C550&sr=8-2"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
}

req = requests.get(url=URL, headers=headers)
req.raise_for_status()
soup = bs4.BeautifulSoup(markup=req.text, features="html.parser")
spans = soup.select(selector=".a-price-whole, .a-price-fraction, .a-price-symbol", limit=3)
product_title = soup.find(name="span", id="productTitle").text.split(":")[0]
price_range = 100
print(spans)
currency = spans[0].text
price = float(f"{spans[1].text}{spans[2].text}")
print(price)
if price <= price_range:
    print("Sending.....")
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.starttls()
        smtp.login(user=email, password=password)
        smtp.sendmail(email, email, msg=f"Subject: Low Price Alert \n\n"
                                        f"The {product_title.strip()} is "
                                        f"at a price of {currency}{price}")
        print("Sent")