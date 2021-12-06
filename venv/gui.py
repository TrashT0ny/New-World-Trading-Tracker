# # Prototype GUI
#   Gui allows simple interface with New World Trading Tracker. Users
#   can enter simplified buy/sell orders, view Order log, and save/load
#   databases.
#   Graphs to be implemented soon, with accompanying filters
# #


import PySimpleGUI as sg
import market_nw
import market_nw as market

#Title Window #####
title_layout = [    [sg.Text('New World Trading Post'), sg.Button('X')],
                    [sg.Button('Buy'), sg.Button('Sell')],
                    [sg.Button('Show Orders')],
                    [sg.Button('Save'), sg.Button('Load')]   ]

title_window = sg.Window('Window Title', title_layout)

#Buy Window #####
def open_buy():
    buy_layout = [  [sg.Text('Buy Order'), sg.Button('X')],
                    [sg.Radio(text='Iron Ore', group_id='item', key='-ore-'), sg.Radio(text='Iron Ingot', group_id='item', key='-ingot-')],
                    [sg.Text('Total', size=(7,1)), sg.Text('Quantity', size=(8,1))],
                    [sg.InputText('', size=(8,1), key='-total-'), sg.InputText('', size=(8,1), key='-quan-')],
                    [sg.Button('Add')]  ]
    buy_window = sg.Window('Buy Order', buy_layout)
    event1, value1 = buy_window.read()
    while True:
        if event1 == 'X':
            break
        if event1 == 'Add':
            if value1['-ore-']:
                market.buy_order(name='Iron Ore', total=int(value1['-total-']), quan=int(value1['-quan-']))
                print('Order placed ', 'iron ore ', value1['-total-'], ' ', value1['-quan-'])
            if value1['-ingot-']:
                market.buy_order(name='Iron Ingot', total=int(value1['-total-']), quan=int(value1['-quan-']))
                print('Order placed ', 'iron ingot ', value1['-total-'], ' ', value1['-quan-'])
            break

    buy_window.close()

#Sell Window #####
def open_sell():
    sell_layout = [[sg.Text('Sell Order'), sg.Button('X')],
                  [sg.Radio(text='Iron Ore', group_id='item', key='-ore-'),
                   sg.Radio(text='Iron Ingot', group_id='item', key='-ingot-')],
                  [sg.Text('Total', size=(7, 1)), sg.Text('Quantity', size=(8, 1))],
                  [sg.InputText('', size=(8, 1), key='-total-'), sg.InputText('', size=(8, 1), key='-quan-')],
                  [sg.Button('Sell')]]
    sell_window = sg.Window('Sell Order', sell_layout)
    event1, value1 = sell_window.read()
    while True:
        if event1 == 'X':
            break
        if event1 == 'Sell':
            if value1['-ore-']:
                market.sell_order(name='Iron Ore', total=0-int(value1['-total-']), quan=0-int(value1['-quan-']))
                print('Order placed ', 'iron ore ', 0-int(value1['-total-']), ' ', 0-int(value1['-quan-']))
            if value1['-ingot-']:
                market.sell_order(name='Iron Ingot', total=0-int(value1['-total-']), quan=0-int(value1['-quan-']))
                print('Order placed ', 'iron ingot ', 0-int(value1['-total-']), ' ', 0-int(value1['-quan-']))
            break

    sell_window.close()

#Orders Window #####
def open_orders():
    orders_layout = [   [sg.Text('Orders'), sg.Button('X')],
                        [sg.Multiline('', size=(30, 4), key='-orders-')] ]
    orders_window = sg.Window('Order Page', orders_layout, finalize=True)
    orders = ''
    for order in market.log:
        if order['name'] != 'init':
            orders += order['name'] + ' ' + str(order['total']) + ' ' + str(order['quantity']) + '\n'
    orders_window['-orders-'].print(orders)
    event1, value1 = orders_window.read()

    while True:

        if event1 == 'X':
            break

    orders_window.close()

#Save Window #####
def open_save():
    save_layout = [ [sg.Text('File Name'), sg.InputText('', size=(12,1), key='-fileName-')],
                    [sg.Button('Save')]  ]
    save_window = sg.Window('Save Data', save_layout)
    event1, value1 = save_window.read()
    while True:
        if event1 == 'Save':
            market.save_order(value1['-fileName-'])
            save_window.close()
            break
    return

#Load Window #####
def open_load():
    load_layout = [ [sg.Text('File Name'), sg.InputText('', size=(12,1), key='-fileName-')],
                    [sg.Button('Load')]  ]
    load_window = sg.Window('Load Data', load_layout)
    event1, value1 = load_window.read()
    while True:
        if event1 == 'Load':
            market.load_order(value1['-fileName-'])
            load_window.close()
            break
    return


# main ###############################################
while True:
    event, values = title_window.read()
    if event == 'Buy':
        title_window.hide()
        open_buy()
        title_window.un_hide()
    if event == 'Sell':
        title_window.hide()
        open_sell()
        title_window.un_hide()
    if event == 'Show Orders':
        title_window.hide()
        open_orders()
        title_window.un_hide()
    if event == 'Save':
        open_save()
        print('Save successful')
    if event == 'Load':
        #clear current vars
        #TODO maybe unnecessary?
        market.gold = 0
        market.log = []
        market.stock = []

        open_load()
        print('Load successful')
    if event == 'X' or sg.WINDOW_CLOSED:
        title_window.close()
        break