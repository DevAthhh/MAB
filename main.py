import time
import random
import json
import requests

def get_market_data():
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    params = {'symbol': 'BTCUSDT'}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            market_data = {
                'price': float(data['lastPrice']),
                'volume': float(data['quoteVolume'])
            }
            return market_data
        else:
            print("Ошибка при получении данных о рынке")
            return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

def make_decision(balance, market_data):
    """Принять решение о покупке или продаже на основе данных о рынке и текущем балансе."""
    # Пример: покупаем, если цена ниже 32000 и у нас есть достаточно USDT
    if market_data['price'] < 32000 and balance > market_data['price']:
        return 'BUY', market_data['price']
    # Продаем, если цена выше 34000 и у нас есть достаточно BTC
    elif market_data['price'] > 34000 and balance > 0:
        return 'SELL', market_data['price']
    else:
        return 'HOLD', market_data['price']

def save_trading_data(decision, price):
    """Записать данные о решении и цене в файл."""
    data = {
        'decision': decision,
        'price': price
    }
    with open('trading_data.json', 'a') as file:
        json.dump(data, file)
        file.write('n')

def trading_bot(starting_balance=10000):
    balance = starting_balance  # Начальный виртуальный баланс в USDT
    
    while True:
        market_data = get_market_data()
        decision, price = make_decision(balance, market_data)
        
        if decision == 'BUY':
            # Покупаем
            balance -= price
            save_trading_data('BUY', price)
            print(f"Покупка по цене {price}. Остаток баланса: {balance}")
        elif decision == 'SELL':
            # Продаем
            balance += price
            save_trading_data('SELL', price)
            print(f"Продажа по цене {price}. Остаток баланса: {balance}")
        else:
            print("Ждем...")
        
        time.sleep(300)  # Пауза в 5 минут перед следующим анализом рынка

# Запускаем торгового бота с начальным балансом 10000 USDT
trading_bot(100)
