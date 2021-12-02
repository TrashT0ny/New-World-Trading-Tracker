## Prototype for New World Trading Tracker
#	Program gives New World players the ability to utilize a more
#	detailed version of trading post data. Until an API is released,
#	users must manually enter their buy/sell orders. In-game market
#	listings will also be viewable if an API allows. Users can have
#	access to analyze, filter, sort data as they wish.
#	Web scraper could be deployed on the side to create a copy of
#	New World Fans database. Store all items in file easily accessed
#	by custom programs.
#   Tax calculator and location data can speed up user input speed
#   and efficiency.

## Version 0.10
#   buy_order(**kwargs)
#   -runs without errors in 8 given cases
#   -assumes name quan and logic expression for other vars exist
#
#   show_totals()
#   -prints current gold and item stock to console
#
#   show_history()
#   -prints timestamp of completed orders
#
##



import time

# Order Prototype
#    name | unit price | tier | gs | gem | perk | rarity | duration | quantity | location | fee | charge | total | time
initOrder = {'name': 'init', 'price': 0, 'tier': 0, 'gs': 0, 'gem': 'none', 'perk': 'none', 'rarity': 'none',
             'duration': 0, 'quantity': 0, 'location': 'none', 'fee': 0, 'charge': 0, 'total': 0, 'time': 'none'}
# Transaction Log
log = [initOrder]
# Current Stock
stock = {'test': 0}
# Gold Expenditure
gold = 0


# buyOrder()
# take input for order, validate, add to log
# required parameters: name, quan, time_0, total|(price&fee)
# name, price, tier, gs, gem, perk, rarity, dur, quan, loc, fee, charge, total
def buy_order(**kwargs):
    global log
    global stock
    global gold

    # # generic user input
    # nName = input('Enter name: ')
    # nPrice = input('Enter price: ')
    # nTier = input('Enter tier: ')
    # nGs = input('Enter gear score: ')
    # nGem = input('Enter gem: ')
    # nPerk = input('Enter perk(s), comma separated: ')
    # nRarity = input('Enter rarity: ')
    # #nDur = input('Enter duration: ')
    # nQuan = input('Enter quantity: ')
    # nLoc = input('Enter location: ')
    # nFee = input('Enter total fee: ')
    # #nCharge = input('Enter charge: ')
    # nTime = time.asctime( time.localtime(time.time()) )
    #
    # # preset user input
    # nName = 'ironOre'
    # nPrice = 0.02
    # nTier = 0
    # nGs = 0
    # nGem = 'none'
    # nPerk = 'none'
    # nRarity = 'common'
    # # nDur = input('Enter duration: ')
    # nQuan = 10
    # nLoc = 'Everfall'
    # nFee = 1
    # # nCharge = input('Enter charge: ')
    # nTime = time.asctime(time.localtime(time.time()))

    # order object creation
    nOrder = {}
    # necessary parameters
    if kwargs['name'] != 'None':
        nOrder['name'] = kwargs['name']
    else:
        print("Order requires an item name")
        return
    if kwargs['quan'] != 'None':
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
    #nOrder['charge'] = charge
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
    return





# sellOrder()


# confirmSell()


# showTotals()
def show_totals():
    print(' Total Gold ' + '{:.2f}'.format(gold))
    print(' Items ')
    for key, value in stock.items():
        if key is not 'test':
            print('  ' + key + " " + str(value))
    return


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


## temporary main
## testing functions
### test passed
# show_history()
# show_totals()
# print('Test 1: all reqs met')
# buy_order(name='Iron Ore', quan=10, total=16, price=1.5, fee=1)
# show_history()
# show_totals()
# print('Test 2: -price ')
# buy_order(name='Iron Ore', quan=5, total=6, fee=1)
# show_history()
# show_totals()
# print('Test 3: -fee')
# buy_order(name='Iron Ore', quan=10, total=12, price=1)
# show_history()
# show_totals()
# print('Test 4: -price -fee')
# buy_order(name='Iron Ore', quan=10, total=13)
# show_history()
# show_totals()
# print('Test 5: -total')
# buy_order(name='Iron Ore', quan=10, price=1.5, fee=1)
# show_history()
# show_totals()
# print('Test 6: -total -price')
# buy_order(name='Iron Ore', quan=10, fee=1)
# show_history()
# show_totals()
# print('Test 7: -total -fee')
# buy_order(name='Iron Ore', quan=10, price=1.5)
# show_history()
# show_totals()
# print('Test 8: -total -fee -price')
# buy_order(name='Iron Ore', quan=10)
# show_history()
# show_totals()
