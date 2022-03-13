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

    f = open(sys.argv[1])

    for line in f:
        line = line.split(' ')[1].split(',')

        print("line after split: ", line)
        req_str = 'http://localhost:9000/' + line[0].lower()

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
        print(data )
        res = requests.put(req_str, json=data)
        print('closing connection')
        res.close()


if __name__ == "__main__":
    main()