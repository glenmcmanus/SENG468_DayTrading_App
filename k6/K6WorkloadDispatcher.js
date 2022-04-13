import http from 'k6/http'
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
//import { OneuserWorkLoad } from './OneuserWorkLoad.txt';

const query_param_definition = {
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

console.log(`${__ENV.FILE}`)
const data2 = open(`${__ENV.FILE}`) //papaparse.parse(open('./OneuserWorkLoad.csv'), { header: false }).data;
//console.log(data2)

export default function () {
    console.log(http.get('http://localhost:5100/DEBUG_DROP'))

    var users = new Set()
    for (var line of data2.split('\n')) {
	if(line == '')
	    continue;

        console.log(line)
        line = String(line).trim().split(' ')[1].split(',')

        var req_str = 'http://localhost:5100/' + String(line[0]).toLowerCase();

	var data={}
        if(line.length > 1){
	    data['command'] = line[0]

            if(line[0] == 'DUMPLOG'){
                if(line.length == 3){
                    data['userID']=line[1]
                    data['filename']=line[2]
                }else
                    data['filename']=line[1]
            } else {
		if(users.has(line[1]) == false){
		    users.add(line[1]);
                    console.log(http.get('http://localhost:5100/REGISTER?userID=' + line[1]));
		}

		if (line.length == 4){
                    data['userID']=line[1]
                    data['stock']=line[2]
                    data['value']=line[3]
                } else {
		    data['userID']=line[1]
		        
		    if (line[0] == 'ADD')
		        data['value']=line[2]
		    else
		        data['stock']=line[2]
		}
            }
        }
	else
	    continue;

        console.log(req_str)
        const headers = { 'Content-Type': 'application/json' };
        const payload = JSON.stringify(data)

        console.log(payload)
	
        const res = http.put(req_str, JSON.stringify(data), { headers: headers });
	console.log(res.body)
    }
}
            
