import json
import time

import requests
import sys

query_param_definition = {
    'ADD':['userid','amount'],
    'QUOTE':['userid', 'StockSymbol'],
    'BUY':['userid','StockSymbol','amount'],
    'COMMIT_BUY':['userid'],
    'CANCEL_BUY':['userid'],
    'SELL':['userid','StockSymbol','amount'],
    'COMMIT_SELL':['userid'],
    'CANCEL_SELL':['userid'],
    'SET_BUY_AMOUNT':['userid','StockSymbol','amount'],
    'CANCEL_SET_BUY':['userid','StockSymbol'],
    'SET_BUY_TRIGGER':['userid','StockSymbol','amount'],
    'SET_SELL_AMOUNT':['userid','StockSymbol','amount'],
    'SET_SELL_TRIGGER':['userid','StockSymbol','amount'],
    'CANCEL_SET_SELL':['userid','StockSymbol'],
    'DUMPLOG':['userid'],
    'DISPLAY_SUMMARY':['userid']

}

data={}
data['transactionNum'] = ""
data['command'] = ""
data['userID'] = ""
data['value'] = ""
data['stock'] = ""
data['filename'] = ""

def main():
    if len(sys.argv) < 2:
        print("You need to pass in the file for dispatch")
        return

    print(requests.get('http://localhost:9000/DEBUG_DROP', timeout=1000))

    f = open(sys.argv[1])

    users = []

    for line in f:
        if line[0] == '#':
            continue

        line = line.rstrip().split(' ')[1].split(',')

        if line[0].lower() == 'sleep':
            print('Sleeping for ', line[1], 's')
            time.sleep(int(line[1]))
            continue

        print("line after split: ", line)
        req_str = 'http://localhost:9000/' + line[0].lower()

        if len(line) > 1:
            if line[1] not in users:
                users.append(line[1])
                register = 'http://localhost:9000/REGISTER?userID=' + line[1]
                requests.get(register, timeout=1000)

        if line[0] == 'DUMPLOG':
            data['command']=line[0]
            data['value'] = ""
            data['stock'] = ""
            if len(line) == 3:
                data['userID']=line[1]
                data['filename']=line[2]
            else:
                data['filename']=line[1]
                data['userID'] = ""
                data['value'] = ""
                data['stock'] = ""
        elif len(line) == 2:
            data['command']=line[0]
            data['userID']=line[1]
            data['value'] = ""
            data['stock'] = ""
            data['filename']=""
        elif len(line) == 3:
            data['command']=line[0]
            data['userID']=line[1]
            if line[0] == 'ADD':
                data['value']=line[2]
                data['stock'] = ""
            else:
                data['stock']=line[2]
                data['value']=""
        elif len(line) == 4:
            data['command']=line[0]
            data['userID']=line[1]
            data['stock']=line[2]
            data['value']=line[3]
            
        print(req_str)
        print(data)
        res = requests.put(req_str, json=data)
        print(res, res.content)
        res.close()


if __name__ == "__main__":
    main()