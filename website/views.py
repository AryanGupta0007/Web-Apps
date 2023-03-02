from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
import json
import keyboard
import sys
import os
import time
import telebot
import datetime
from datetime import timedelta
from .models import User
from . import db 
views = Blueprint("views", __name__)
apiToken = "6031902860:AAEsuPRks6KfXlpkeKWcgEQ_lYtm_QTsomM"

date_list = []
# bot = telebot.TeleBot(TELEGRAM_BOT_API)
# @bot.message_handler(commands=["Alert"])
# def alert(message):
#     bot.reply_to(message, "")
def send_message_to_group(message):
    # send_message = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id=838452194&text={message}"
    chatID = '-956779181'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})


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



def alert_user(current_price, alert_price, notification, email):
            
    notification = session["notification"] 
    alert_price = session["alert_price"] 
    symbol = session["symbol"] 
    initial_price = session["initial_price"] 
        
    # date_time = Alert_Time(date_time=current_time, user.id=)
    # db.session()
    # email = session["email"]

    current_date = datetime.datetime.now().strftime("%d:%m:%Y")
    user = User.query.filter_by(email=email).first()
    # os.system("cls")
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")         
        
    msg = f"Dear {user.name} I suggest action (buy or sell) \t as the price currently is: ${current_price}\t which is {notification} to {alert_price}"
    if current_date not in date_list:
    
        send_message_to_group(msg)
        date_list.append(current_date)
        print(date_list)
        time.sleep(10)
    else:
        print(msg)    
    
@views.route("/")
def home():
    return render_template("base.html")

@views.route("/display", methods=["POST", "GET"])
def display():
    # if request.method == "POST":
    #     return render_template("display.html")
    
    time.sleep(5)
    return redirect(url_for("views.update_price"))
    
@views.route("/update_price", methods=["POST", "GET"])
def update_price():
        notification = session["notification"] 
        alert_price = session["alert_price"] 
        symbol = session["symbol"] 
        initial_price = session["initial_price"] 
        email = session["email"]

        os.system("cls")
        print("Press \"Q\" to exit the program")
        print("Press \"S\" to see the price stats")
    
      
        URL_for_dollar = f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

        prices_dollar = []
        times = []
                    
        # os.system("cls")
        print(f"Intial Price: {round(float(initial_price), 2)} Alert Price: {notification} to {alert_price}\n\n")
        # time.sleep(10)
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
                
                alert_user(current_price, alert_price, notification, email)
                
            else:
                do_nothing(price_dollar, alert_price, symbol, difference)
                
                    
                
        elif (notification == "lower"):
            if (alert_price > current_price):
                alert_user(current_price, alert_price, notification, email)
            else:
                do_nothing(price_dollar, alert_price, symbol, difference)
                
        return redirect(url_for("views.display"))

    
    

@views.route("/home", methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        email = request.args.get("email")
        session["email"] = email    
        return render_template("home.html")

    elif request.method == "POST":
        
        symbol = request.form.get("Symbol")
        alert_price = request.form.get("Alert-Price")
        notification= request.form.get("Notification")
        session["notification"] = notification
        session["alert_price"] = alert_price
        session["symbol"] = symbol
        email = session["email"]
        os.system("cls")
        print("Press \"Q\" to exit the program")
        print("Press \"S\" to see the price stats")
    
        try:
            get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
            initial_price = get_data["price"]
            session["initial_price"] = initial_price
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
                    pass                    
                else:
                    do_nothing(price_dollar, alert_price, symbol, difference)
                        
                    
            elif (notification == "lower"):
                if (alert_price > current_price):
                    pass
                else:
                    do_nothing(price_dollar, alert_price, symbol, difference)
                    
            return redirect(url_for("views.display"))

