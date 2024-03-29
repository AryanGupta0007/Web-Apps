from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
import json
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

alerts_list = []
user_entry = {}
alerts = []
# n =  6
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




def do_nothing():
   pass         

def take_action():                    
    notification = session["notification"]
    # notification = notification.lower() 
    alert_price = session["alert_price"] 
    symbol = session["symbol"] 
    # symbol = symbol.upper()
    initial_price = session["initial_price"] 
    email = session["email"]
    os.system("cls")
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")

    
    URL_for_dollar = f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

                
    
    get_Data_Dollar = requests.get(URL_for_dollar).json()
    price_dollar = get_Data_Dollar["price"]
    
    # greatest_value = store_highest_value(price)
    current_price = float(price_dollar)
    alert_price = float(alert_price)
    difference = current_price - alert_price
    difference = round(difference, 2)
    
    if (notification == "greater"):
        
        if (alert_price < current_price):
            
            alert_user(current_price, alert_price, notification, email)
            
        else:
            do_nothing()
            
                
            
    elif (notification == "lower"):
        if (alert_price > current_price):
            alert_user(current_price, alert_price, notification, email)
        else:
            do_nothing()
            
    


def alert_user(current_price, alert_price, notification, email):
            
    notification = session["notification"] 
    alert_price = session["alert_price"] 
    symbol = session["symbol"] 
    initial_price = session["initial_price"] 
    current_alert = f"{symbol}{notification} to ${alert_price}"
    frequency = session["frequency"]
    if frequency == "1 Minute":
        frequency = 1
    elif frequency == "5 Minutes":
        frequency = 5
    elif frequency == "10 Minutes":
        frequency = 10
    elif frequency == "30 Minutes":
        frequency = 30
    elif frequency == "1 Hour":
        frequency = 60
    elif frequency == "3 Hours":
        frequency = 180
    elif frequency == "12 Hours":
        frequency = 720
    elif frequency == "1 Day":
        frequency = 1440
            
    print(current_alert)
    # symbol = symbol.upper()
    # notification = notification.lower()
    current_date = datetime.datetime.now().strftime("%H:%M %d:%m:%Y")
    current_date_ob = datetime.datetime.now().strptime( current_date, "%H:%M %d:%m:%Y")
    user = User.query.filter_by(email=email).first()
    # os.system("cls")
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")    
    email = user.email     
    current_entry = {user.email : [alert_price, current_date_ob, symbol, notification]}        
    msg = f"Dear {user.name} (email = {user.email}) I suggest action (buy or sell) on {symbol} \t as the price currently is: ${current_price}\t which is {notification} to ${alert_price}"
    print(current_entry)
    
    print(alerts_list)
    if current_entry not in alerts_list:
    
        send_message_to_group(msg)
        # current_date_ob = datetime.strptime(current_date, "%H:%M:%S %d:%m:%Y")
        for x in range(0, frequency):
            
            notif_time = current_date_ob + timedelta(minutes=x)
            user_entry = {user.email : [alert_price, notif_time, symbol, notification]} 
        
            alerts_list.append(user_entry)
            

        print(alerts_list)
        last_alert = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        alerts.append(last_alert)
        # time.sleep(10)
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

    if request.method == "GET":
        get_data_btc = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        get_data_xrp = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=XRPUSDT").json()
        get_data_doge = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=DOGEUSDT").json()
        get_data_eth = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
        get_data_bnb = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=BNBUSDT").json()
        notification = session["notification"]
        alert_price = session["alert_price"]
        email = session["email"]
        symbol = session["symbol"]
        frequency = session["frequency"]
        take_action()
        current_alert = f"{symbol} {notification} to ${alert_price} and alert frequency = {frequency}"
        try:
            
            last_alert = alerts[-1]
        except:
            last_alert = "No alerts till now"
            
        return render_template("home2.html", initial_price_btc=float(get_data_btc["price"]), initial_price_eth=float(get_data_eth["price"]), initial_price_bnb=float(get_data_bnb["price"]), initial_price_doge=float(get_data_doge["price"]), initial_price_xrp=float(get_data_xrp["price"]), current_alert=current_alert, last_alert=last_alert, email=email)


@views.route("/home", methods=["GET", "POST"])
def homepage():
    if request.method == "GET":
        alerts.clear()
        alerts_list.clear()
        get_data_btc = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        get_data_xrp = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=XRPUSDT").json()
        get_data_doge = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=DOGEUSDT").json()
        get_data_eth = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()
        get_data_bnb = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol=BNBUSDT").json()
        
        email = request.args.get("email")
        session["email"] = email    
        return render_template("home.html", initial_price_btc=float(get_data_btc["price"]), initial_price_eth=float(get_data_eth["price"]), initial_price_bnb=float(get_data_bnb["price"]), initial_price_doge=float(get_data_doge["price"]), initial_price_xrp=float(get_data_xrp["price"]))

    elif request.method == "POST":
        symbol = request.form.get("Symbol")
        alert_price = request.form.get("Alert-Price")
        notification= request.form.get("Notification")
        symbol = symbol.upper().strip()
        notification = notification.lower().strip()
        frequency = request.form.get("frequency")
        session["notification"] = notification
        session["alert_price"] = alert_price
        session["symbol"] = symbol
        session["frequency"] =  frequency
        email = session["email"]
        try:
            alert_price = float(alert_price)
            if (alert_price < 0):
                raise ValueError("")
            
        except:
            flash("Invalid alert price Please enter a numeric value greater than 0")
            return redirect(url_for("views.homepage", email=email))
        try:
            if (notification != "greater" and notification != "lower"):
                raise Exception("")
        except:
            flash("Invalid notification value please enter valid notification value example: greater to lower")
            return redirect(url_for("views.homepage", email=email))

        try:    
            get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
            initial_price = get_data["price"]
            session["initial_price"] = initial_price
        except:
            flash("Invalid Symbol please enter a valid symbol. example: XRP, BTC, DOGE")
            return redirect(url_for("views.homepage", email=email))
        # os.system("cls")
        # print(f"Intial Price: {round(float(initial_price), 2)} Alert Price: {notification} to {alert_price}\n\n")
        # take_action()
        return redirect(url_for("views.update_price", email=email))
