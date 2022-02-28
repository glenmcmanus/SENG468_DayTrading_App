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

def main():
    if len(sys.argv) < 2:
        print("You need to pass in the file for dispatch")
        return

    f = open(sys.argv[1])

    for line in f:
        line = line.split(' ')[1].split(',')

        print("line after split: ", line)

        req_str = 'http://localhost:9000/' + line[0] + '?'

        if line[0] == 'DUMPLOG':
            if len(line) == 2:
                #do req for all
                print('dumplog output: ', line[1])
            elif len(line) == 3:
                print('dumplog for user', line[1], ' output: ', line[2])
                req_str += '&userid' + line[1]
            else:
                print('malformed dumplog request')
        else:
            param_names = query_param_definition[line[0]]
            line = line[1:]
            for i in range(0, len(line)):
                req_str += param_names[i] + '=' + line[i] + '&'

            req_str = req_str.rstrip('&')

            print(req_str)

        r = requests.get(req_str)


if __name__ == "__main__":
    main()