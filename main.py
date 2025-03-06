import time
import random
import threading

NUM_TICKERS = 1024

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type.lower()
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.timestamp = time.time()

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

order_books = [OrderBook() for i in range(NUM_TICKERS)]


def ticker_to_index(ticker):
    return sum(ord(c) for c in ticker) % NUM_TICKERS


def addOrder(order_type, ticker, quantity, price):
    index = ticker_to_index(ticker)
    order = Order(order_type, ticker, quantity, price)
    if order.order_type == 'buy':
        order_books[index].buy_orders.append(order)
    elif order.order_type == 'sell':
        order_books[index].sell_orders.append(order)
    else:
        print("Invalid order type")
    print(f"Added {order_type.upper()} order for {ticker}: Qty {quantity} at Price {price}")


def matchOrder():
    for index in range(NUM_TICKERS):
        ob = order_books[index]
        while ob.buy_orders and ob.sell_orders:
            best_buy = max(ob.buy_orders, key=lambda order: (order.price, -order.timestamp))
            best_sell = min(ob.sell_orders, key=lambda order: (order.price, order.timestamp))
            if best_buy.price >= best_sell.price:
                trade_qty = min(best_buy.quantity, best_sell.quantity)
                trade_price = best_sell.price
                print(f"Trade executed on ticker {best_buy.ticker}: Qty {trade_qty} at Price {trade_price}")
                best_buy.quantity -= trade_qty
                best_sell.quantity -= trade_qty
                if best_buy.quantity == 0:
                    ob.buy_orders.remove(best_buy)
                if best_sell.quantity == 0:
                    ob.sell_orders.remove(best_sell)
            else:
                break

# Random order generator
def random_order_generator():
    tickers = ["AAPL", "GOOG", "MSFT"]
    order_types = ["buy", "sell"]
    while True:
        order_type = random.choice(order_types)
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = random.randint(10, 500)
        addOrder(order_type, ticker, quantity, price)
        time.sleep(random.uniform(0.1, 0.5))

def order_matching_engine():
    while True:
        matchOrder()
        time.sleep(0.1)

def run_simulation():
    num_broker_threads = 2
    for _ in range(num_broker_threads):
        threading.Thread(target=random_order_generator, daemon=True).start()
    threading.Thread(target=order_matching_engine, daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation interrupted.")


if __name__ == "__main__":
    run_simulation()
