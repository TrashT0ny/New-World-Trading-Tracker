# # Prototype for New World Trading Tracker
# 	Program gives New World players the ability to utilize a more
# 	detailed version of trading post data. Until an API is released,
# 	users must manually enter their buy/sell orders. In-game market
# 	listings will also be viewable if an API allows. Users can have
# 	access to analyze, filter, sort data as they wish.
# 	Web scraper could be deployed on the side to create a copy of
# 	New World Fans database. Store all items in file easily accessed
# 	by custom programs.
#   Tax calculator and location data can speed up user input speed
#   and efficiency.
# #

# # Version 0.3
#   buy_order(**kwargs)
#   -runs without errors in 8 given cases
#   -assumes name quan and logic expression for other vars exist
#
#   sell_orders(**kwargs)
#   -runs without errors in 9 given cases
#   -assumes name quan and logic expression for other vars exist
#
#   show_totals()
#   -prints current gold and item stock to console
#
#   show_history()
#   -prints timestamp of completed orders
#
#   save_order(fileName)
#
#   load_order(fileName)
#
# #


import time
import pickle

# Order Prototype
#    name | unit price | tier | gs | gem | perk | rarity | duration | quantity | location | fee | charge | total | time
# initOrder = {'name': 'init', 'price': 0, 'tier': 0, 'gs': 0, 'gem': 'none', 'perk': 'none', 'rarity': 'none',
#             'duration': 0, 'quantity': 0, 'location': 'none', 'fee': 0, 'charge': 0, 'total': 0, 'time': 'none'}
# Transaction Log
import market_nw

log = []
# Current Stock
stock = {}
# Gold Expenditure
gold = 0


# buyOrder()
# take input for order, validate, add to log
# required parameters: name, quan, time_0, total|(price&fee)
# name, price, tier, gs, gem, perk, rarity, dur, quan, loc, fee, total
def buy_order(**kwargs):
    global log
    global stock
    global gold

    # order object creation
    nOrder = {}
    # necessary parameters
    if 'name' in kwargs:
        nOrder['name'] = kwargs['name']
    else:
        print("Order requires an item name")
        return
    if 'quan' in kwargs:
        nOrder['quantity'] = kwargs['quan']
    else:
        print("Order requires a quantity")
        return

    # total cost validator
    #   validator requires some way to calculate
    #   total cost after tax unless given.
    #   orders missing tax are illegal to prevent
    #   DCA(dollar cost average) underestimated value
    # LOGIC: T|(P&F)
    if 'total' not in kwargs:
        if 'price' not in kwargs and 'fee' not in kwargs:
            print("Order requires either total cost, or unit price and fee")
            return
        elif 'price' in kwargs and 'fee' in kwargs:
            kwargs['total'] = kwargs['price'] * kwargs['quan'] + kwargs['fee']
        else:
            print("Order requires either total cost, or unit price and fee")
            return
    else:
        if 'price' not in kwargs and 'fee' not in kwargs:
            kwargs['price'] = kwargs['total'] / kwargs['quan']
            # fee remains empty to show price is after tax
        elif 'price' not in kwargs:
            kwargs['price'] = (kwargs['total'] - kwargs['fee']) / kwargs['quan']
        elif 'fee' not in kwargs:
            kwargs['fee'] = kwargs['total'] - (kwargs['price'] * kwargs['quan'])

    try:
        nOrder['price'] = kwargs['price']
    except:
        nOrder['price'] = 'None'
    try:
        nOrder['gs'] = kwargs['gs']
    except:
        nOrder['gs'] = 'None'
    try:
        nOrder['gem'] = kwargs['gem']
    except:
        nOrder['gem'] = 'None'
    try:
        nOrder['perk'] = kwargs['perk']
    except:
        nOrder['perk'] = 'None'
    try:
        nOrder['rarity'] = kwargs['rarity']
    except:
        nOrder['rarity'] = 'None'
    try:
        nOrder['duration'] = kwargs['dur']
    except:
        nOrder['duration'] = 'None'
    try:
        nOrder['location'] = kwargs['loc']
    except:
        nOrder['location'] = 'None'
    try:
        nOrder['fee'] = kwargs['fee']
    except:
        nOrder['fee'] = 'None'
    # nOrder['charge'] = charge
    nOrder['total'] = kwargs['total']
    nOrder['time'] = time.asctime(time.localtime(time.time()))

    # add transaction to log, update stock/gold
    log += [nOrder]
    try:
        stock[nOrder['name']] += nOrder['quantity']
    except:
        stock[nOrder['name']] = nOrder['quantity']
    gold -= (kwargs['price'] * nOrder['quantity'])
    if nOrder['fee'] != 'None':
        gold -= nOrder['fee']
    print([gold, stock, log])
    return


# sellOrder()
# required parameters: name, quan, time_0, fee, net price or gross price and unit charge
# name, gross price, net price, tier, gs, gem, perk, rarity, duration, quantity, location, fee, charge, total, time
def sell_order(**kwargs):
    global log
    global stock
    global gold

    # order object creation
    nOrder = {}
    # necessary parameters
    if 'name' in kwargs:
        nOrder['name'] = kwargs['name']
    else:
        print("Order requires an item name")
        return
    if 'quan' in kwargs:
        nOrder['quantity'] = kwargs['quan']
    else:
        print("Order requires a quantity")
        return

    # gold calculations
    if 'fee' not in kwargs:
        print("Listing fee required")
        return
    else:
        if 'charge' not in kwargs:
            if 'nPrice' not in kwargs:
                print('Charge and gross price, or net price required')
                return
            nOrder['nPrice'] = kwargs['nPrice']
            if 'price' in kwargs:
                nOrder['price'] = kwargs['price']
                nOrder['charge'] = kwargs['price'] - kwargs['nPrice']
            else:
                nOrder['nPrice'] = kwargs['nPrice']
        else:
            nOrder['charge'] = kwargs['charge']
            if 'price' not in kwargs and 'nPrice' not in kwargs:
                print('Charge and gross price, or net price required')
                return
            elif 'price' not in kwargs:
                nOrder['price'] = kwargs['charge'] + kwargs['nPrice']
                nOrder['nPrice'] = kwargs['nPrice']
            elif 'nPrice' not in kwargs:
                nOrder['nPrice'] = kwargs['price'] - kwargs['charge']
                nOrder['price'] = kwargs['price']
            else:
                nOrder['nPrice'] = kwargs['nPrice']
                nOrder['price'] = kwargs['price']
        gold -= kwargs['fee']
        nOrder['fee'] = kwargs['fee']

    # optional parameters
    try:
        nOrder['gs'] = kwargs['gs']
    except:
        nOrder['gs'] = 'None'
    try:
        nOrder['gem'] = kwargs['gem']
    except:
        nOrder['gem'] = 'None'
    try:
        nOrder['perk'] = kwargs['perk']
    except:
        nOrder['perk'] = 'None'
    try:
        nOrder['rarity'] = kwargs['rarity']
    except:
        nOrder['rarity'] = 'None'
    try:
        nOrder['duration'] = kwargs['dur']
    except:
        nOrder['duration'] = 'None'
    try:
        nOrder['location'] = kwargs['loc']
    except:
        nOrder['location'] = 'None'

    nOrder['time'] = time.asctime(time.localtime(time.time()))
    # add order to log, quantity not affected until sell order confirmed
    log += [nOrder]

    return


# confirmSell()


# showTotals()
def show_totals():
    print(' Total Gold ' + '{:.2f}'.format(gold))
    print(' Items ')
    for key, value in stock.items():
        if key != 'test':
            print('  ' + key + ' ' + str(value))


# crunchDCA()


# showHistory()
def show_history():
    if len(log) > 1:
        for order in log:
            if order['time'] != 'none':
                print(' order:: ' + order['time'])
    else:
        print('Log is empty.')
    return


# saveOrder()
# doesn't overwrite
def save_order(fileName):
    db = {'gold': gold, 'stock': stock, 'log': log}
    dbfile = open('saves/' + fileName, 'ab')
    pickle.dump(db, dbfile)
    dbfile.close()
    return


# loadOrder()
def load_order(fileName):
    try:
        dbfile = open('saves/' + fileName, 'rb')
    except:
        print('File Not Found')
        return
    db = pickle.load(dbfile)
    print(db)
    market_nw.gold = db['gold']
    market_nw.stock = db['stock']
    market_nw.log = db['log']
    dbfile.close()
    return

