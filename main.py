from abc import ABC, abstractmethod
from helium import start_chrome, kill_browser
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
import validators
from time import sleep
from threading import Thread
import re
import requests
import os


class PriceTracker(ABC):
    """
    Base class for Price Trackers.
    """
    email = "your email here"
    password = "your email password here"
    removals = re.compile(r"₹|,|[$]")

    def __init__(self, product_name: str, product_url: str, desired_price: int) -> None:
        """
        Constructor.
        """
        if not validators.url(product_url):
            raise Exception("Invalid URL!")

        self.product_url = product_url
        self.set_price = desired_price
        self.product_name = product_name
        self.price = None

    @abstractmethod
    def get_price(self):
        """
        Fetches the latest price of the product.
        """
        pass

    @staticmethod
    def send_mail(your_email:str, your_password:str, subject: str, body: str):
        """
        Sends mail for the given price.
        """
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email,
                        your_email, f"Subject: {subject}\n\n{body}")
        server.quit()
        print("Mail sent")

    @abstractmethod
    def write_to_file(self):
        """
        Write content to a text file.
        """
        pass

    def track_price(self):
        """
        Tracks price for a given product against the set price.
        """
        while True:
            self.get_price()
            if self.price == None:
                print("Unable to fetch the latest price!")
                os._exit(1)

            if self.set_price >= self.price:
                print("Price low for", self.product_name)
                self.write_to_file()
                self.send_mail(self.email, self.password, f"Price down for {self.product_name}",f"Dear sir,\nThe price for `{self.product_name}` is now {self.price} which is less than or equal to what you desired, {self.set_price}! Visit {self.product_url} for more info.")
                os._exit(0)

            else:
                self.write_to_file()

            sleep(60)


class AmazonPriceTracker(PriceTracker):
    """
    Helps poor people by notifying them when the price for their favorite product on Amazon is less than what they desired.
    """

    def get_price(self):
        """
        Fetches price for given product on Amazon.
        """
        driver = start_chrome(self.product_url)
        html = driver.page_source.replace("&nbsp;", "")
        kill_browser()
        soup = BeautifulSoup(html, "html5lib")
        price = soup.find("span", {"id": "priceblock_ourprice"})
        if price == None:
            price = soup.find("span", {"id": "priceblock_dealprice"}).string
        price = (re.sub(self.removals, "", price)).replace("\\xa", "")
        self.price = int(float(price))

    def write_to_file(self):
        """
        Writes datetime and price to a file.
        """
        now = datetime.now().strftime("%d-%m-%y %H:%M")
        content = f"{now} --> Amazon --> {self.price}\n"
        print(content)
        with open(f"{self.product_name}.prices", "a") as f:
            f.write(content)

    def run(self):
        self.track_price()


class FlipkartPriceTracker(PriceTracker):
    """
    Helps poor people by notifying them when the price of their favorite product on Flipkart is less than what they desired.
    """

    def get_price(self):
        """
        Fetches price for given product on Flipkart.
        """
        r = requests.get(self.product_url)
        soup = BeautifulSoup(r.content, "html5lib")
        price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).string
        price = re.sub(self.removals, "", price)
        self.price = int(price)

    def write_to_file(self):
        """
        Writes datetime and price to a file.
        """
        now = datetime.now().strftime("%d-%m-%y %H:%M")
        content = f"{now} --> Flipkart --> {self.price}\n"
        print(content)
        with open(f"{self.product_name}.prices", "a") as f:
            f.write(content)

    def run(self):
        self.track_price()


class MultipleStorePriceTracker():
    """
    Tracks prices for two stores at a time (Amazon and Flipkart) and notifies when either of them is less than the desired price.
    """

    def __init__(self, product_name:str, amazon_url:str, flipkart_url:str, desired_price:int) -> None:
        self.product = product_name
        self.fkturl = flipkart_url
        self.azurl = amazon_url
        self.set_price = desired_price

    def track_multiple(self):
        fktt = FlipkartPriceTracker(self.product, self.fkturl, self.set_price)
        azt = AmazonPriceTracker(self.product, self.azurl, self.set_price)
        t1 = Thread(target=fktt.run)
        t2 = Thread(target=azt.run)
        t1.start()
        t2.start()


def check_internet():
    try:
        requests.get("https://google.com")
    
    except Exception:
        raise Exception("Make sure you're connected to internet!")



if __name__ == "__main__":
    check_internet()
    print("Welcome to the Ecommerce Price Tracker! A tool which you can use to track prices for a given product on Amazon and Flipkart.\n")

    track_opt = input("Where to track prices?\n 1. Amazon \n 2. Flipkart \n 3. Both\n")

    if track_opt == "1":
        try:
            product_name = input("Enter product name: ")
            product_url = input("Enter the product url: ")
            desired_price = int(input("Enter the desired price (you'll be notified when this price is lower than the product price): "))
            azt = AmazonPriceTracker(product_name, product_url, desired_price)
            azt.run()

        except Exception as e:
            print(e)

    elif track_opt == "2":
        try:
            product_name = input("Enter product name: ")
            product_url = input("Enter the product url: ")
            desired_price = int(input("Enter the desired price (you'll be notified when this price is lower than the product price): "))
            fkt = FlipkartPriceTracker(product_name, product_url, desired_price)
            fkt.run()
        
        except Exception as e:
            print(e)

    elif track_opt == "3":
        try:
            product_name = input("Enter product name: ")
            azurl = input("Enter the product url on Amazon: ")
            fkturl = input("Enter the product url on Flipkart: ")
            desired_price = int(input("Enter the desired price (you'll be notified when this price is lower than the product price): "))
            mspt = MultipleStorePriceTracker(product_name, azurl, fkturl, desired_price)
            mspt.track_multiple()

        except Exception as e:
            print(e)

    else:
        print("Invalid input!")