import requests
import json
import keyboard
import sys
import os
# import time
# from datetime import datetime
# import pandas as pd
# import matplotlib.pyplot as plt
# from tabulate import tabulate

os.system("cls")
print("Press \"Q\" to exit the program")
print("Press \"S\" to see the price stats")
if __name__ == "__main__":
    symbol, initial_price, alert_price, notification = get_user_input()
else:
    try:
        get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
        initial_price = get_data["price"]
        
    except:
        sys.exit("Sorry you entered an invalid coin name. Retry")
    
URL_for_dollar = f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

prices_dollar = []
times = []
            
os.system("cls")
print(f"Intial Price: {round(float(initial_price), 2)} Alert Price: {notification} to {alert_price}\n\n")

while True:
    symbol_data = {"price":prices_dollar, "time":times}    
    get_Data_Dollar = requests.get(URL_for_dollar).json()
    # get_current_time = datetime.now()
    # get_current_time = time.strftime("%H:%M:%S", time.localtime())
    
    # times.append(get_current_time)
    # # df = pd.DataFrame(symbol_data)
    # print(times, end="\r")
    # print(get_Data_Dollar)
    # print(get_Data_Dollar)
    price_dollar = get_Data_Dollar["price"]
    # symbol = get_Data_Dollar["symbol"]
    prices_dollar.append(price_dollar)
    
    # greatest_value = store_highest_value(price)
    current_price = float(price_dollar)
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

    elif (notification == "equal"):
        if (alert_price == current_price):
            alert_user(current_price, alert_price, notification) 
        else:
            do_nothing(price_dollar, alert_price, symbol, difference)
            # carriage return used to return the curson of the mouse to the initial position
    # print(price_stats(prices))
    if (keyboard.is_pressed("s")):
        os.system("cls")
        print(price_stats(prices_dollar))
        time.sleep(5)
        continue
    
    if (keyboard.is_pressed("q")):
        os.system("cls")
        print(f"{price_stats(prices_dollar)}")
        break    


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

def get_user_input():
    # get symbols and alert price from the user
    print("""Examples of symbols of some Currencies: \nETH: Ethereum\nBTC: "Bitcoin """)
    symbol = input("Enter the Symbol of the Currency you want to track: ").upper().strip()
    try:
            get_data = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
            initial_price = get_data["price"]
            
    except:
            sys.exit("Sorry you entered an invalid coin name. Retry")
            
        
        
    print(f"intial price: ${round(float(initial_price), 2)}")
    alert_price = input("Enter the alert price: $")
    notification = input(f"Would you like to be notified when the price is \"greater\" \"lower\"   or \"equal\"  to {alert_price} ").lower()
    

    return symbol, initial_price, float(alert_price), notification        



def do_nothing(price_dollar, alert_price, symbol, difference):
    os.system("cls") 
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")         
    
            
    print(f"Symbol: {symbol}\t\t Current Price: ${round(float(price_dollar), 2)}\t\tAlert Price: ${alert_price}\t Difference from alert price: ${difference}\t ", end = "\r")
    sys.stdout.flush()



def alert_user(current_price, alert_price, notification):
    os.system("cls")
    print("Press \"Q\" to exit the program")
    print("Press \"S\" to see the price stats")         
        
    print(f"I suggest action (buy or sell) \t as the price currently is: ${current_price}\t which is {notification} to {alert_price}", end = "\n")
    sys.stdout.flush()

        
if __name__ == "__main__":
    main()    