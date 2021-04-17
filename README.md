# Ecommerce-Price-Tracker

**Ecommerce-Price-Tracker** is a python utility which notifies you when the price of the product on your wishlist is less than what you desired. It has support for price tracking on Amazon and Flipkart.

## Features
- Track prices of a product on Amazon
- Track prices of a product on Flipkart
- Track prices of a product on both Amazon and Flipkart simultaneously
- Get notified via emails when the price is lower than desired price

## Setup
To use the **Ecommerce-Price-Tracker**, you just need the product name, product url and the desired price.

* Product name - The name of the product you want to track
* Product URL - The URL of the product page on Amazon or Flipkart
* Desired price - The least price you want to buy the product at. When this price will be lower or eqaul to the actual price of the product, you'll be notified via a email.

**Also provide your email and email password in the `credentials.json` file, and enable less secure apps on your email service provider before running the program.**

## Dependencies
*External modules used:*
- beautifulsoup4
- helium
- requests 
- validators 
- html5lib 

Download all the above mentioned modules at once by executing the command `pip install -r requirements.txt` on the terminal.


## Installation
### Using Git
Type the following command in your Git Bash:

- For SSH:
```git clone git@github.com:Shravan-1908/Ecommerce-Price-Tracker.git```
- For HTTPS: ```git clone https://github.com/Shravan-1908/Ecommerce-Price-Tracker.git```

The whole repository would be cloned in the directory you opened the Git Bash in.

### Using GitHub ZIP download
You can alternatively download the repository as a zip file using the
GitHub **Download ZIP** feature by clicking [here](https://github.com/Shravan-1908/Ecommerce-Price-Tracker/archive/master.zip).