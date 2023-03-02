from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
import json
import keyboard
import sys
import os
import time
import telebot

views = Blueprint("views", __name__)
apiToken = "6031902860:AAEsuPRks6KfXlpkeKWcgEQ_lYtm_QTsomM"

# bot = telebot.TeleBot(TELEGRAM_BOT_API)
# @bot.message_handler(commands=["Alert"])
# def alert(message):
#     bot.reply_to(message, "")
def send_message_to_group(message):
    # send_message = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id=838452194&text={message}"
    chatID = '-838452194'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    print(response.text)


def price_stats(prices):
    current_price = prices[0]
    lowest_price = prices[0]
        
    for x in range(1, len(prices)):
        if (current_price < prices[x]):
            current_price = prices[x]
    
    for x in range(1, len(prices)):
        if (lowest_price > prices[x]):
            lowest_price = prices[x]
    lowest_price = float(lowest_price)
    highest_price = float(current_price)
    return f"Highest Price: ${highest_price}\nLowest Price: ${lowest_price}"




def do_nothing(price_dollar, alert_price, symbol, difference):
    os.system("cls") 
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")         
    
            
    print(f"Symbol: {symbol}\t\t Current Price: ${round(float(price_dollar), 2)}\t\tAlert Price: ${alert_price}\t Difference from alert price: ${difference}\t", end="")
    sys.stdout.flush()



def alert_user(current_price, alert_price, notification):
    os.system("cls")
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")         
        
    msg = f"I suggest action (buy or sell) \t as the price currently is: ${current_price}\t which is {notification} to {alert_price}"
    send_message_to_group(msg)
    sys.stdout.flush()


@views.route("/")
def home():
    return render_template("base.html")

@views.route("/display", methods=["POST", "GET"])
def display():
    time.sleep(10)
    # if request.method == "POST":
    #     return render_template("display.html")
    return render_template("display.html")
    
@views.route("/update_price", methods=["POST", "GET"])
def update_price():
        notification = session["notification"] 
        alert_price = session["alert_price"] 
        symbol = session["symbol"] 
        os.system("cls")
        print("Press \"Q\" to exit the program")
        print("Press \"S\" to see the price stats")
    
        try:
            get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
            initial_price = get_data["price"]
            
        except:
            sys.exit("Sorry you entered an invalid coin name. Retry")

        URL_for_dollar = f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

        prices_dollar = []
        times = []
                    
        # os.system("cls")
        print(f"Intial Price: {round(float(initial_price), 2)} Alert Price: {notification} to {alert_price}\n\n")
        time.sleep(10)
        symbol_data = {"price":prices_dollar, "time":times}    
        get_Data_Dollar = requests.get(URL_for_dollar).json()
        price_dollar = get_Data_Dollar["price"]
        # symbol = get_Data_Dollar["symbol"]
        prices_dollar.append(price_dollar)
        
        # greatest_value = store_highest_value(price)
        current_price = float(price_dollar)
        alert_price = float(alert_price)
        difference = current_price - alert_price
        difference = round(difference, 2)
        
        if (notification == "greater"):
            
            if (alert_price < current_price):
                alert_user(current_price, alert_price, notification)
                
            else:
                msg = do_nothing(price_dollar, alert_price, symbol, difference)
                flash(msg)
                return redirect(url_for("views.display"))
                    
                
        elif (notification == "lower"):
            if (alert_price > current_price):
                alert_user(current_price, alert_price, notification)
            else:
                msg = do_nothing(price_dollar, alert_price, symbol, difference)
                flash(msg)
                return redirect(url_for("views.display"))

    
    

@views.route("/home", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        
        symbol = request.form.get("Symbol")
        alert_price = request.form.get("Alert-Price")
        notification= request.form.get("Notification")
        session["notification"] = notification
        session["alert_price"] = alert_price
        session["symbol"] = symbol

        os.system("cls")
        print("Press \"Q\" to exit the program")
        print("Press \"S\" to see the price stats")
    
        try:
            get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
            initial_price = get_data["price"]
            
        except:
            sys.exit("Sorry you entered an invalid coin name. Retry")
        
        prices_dollar = []
        times = []
                    
        os.system("cls")
        print(f"Intial Price: {round(float(initial_price), 2)} Alert Price: {notification} to {alert_price}\n\n")
        while True:
            URL_for_dollar = f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    
        
            # time.sleep(5)
            symbol_data = {"price":prices_dollar, "time":times}    
            get_Data_Dollar = requests.get(URL_for_dollar).json()
            price_dollar = get_Data_Dollar["price"]
            # symbol = get_Data_Dollar["symbol"]
            prices_dollar.append(price_dollar)
            
            # greatest_value = store_highest_value(price)
            current_price = float(price_dollar)
            alert_price = float(alert_price)
            difference = current_price - alert_price
            difference = round(difference, 2)
            if (notification == "greater"):
                
                if (alert_price < current_price):
                    alert_user(current_price, alert_price, notification)
                    
                else:
                    do_nothing(price_dollar, alert_price, symbol, difference)
                        
                    
            elif (notification == "lower"):
                if (alert_price > current_price):
                    alert_user(current_price, alert_price, notification)
                else:
                    do_nothing(price_dollar, alert_price, symbol, difference)
                    
            

    return render_template("home.html")
