def generate_userCommand(timestamp, server, transactionNum, command, username = None, stockSymbol = None, filename = None, funds = None):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    command_string = "        <command>" + command + "</command>\n"
    if username != None:
        username_string = "        <username>" + username + "</username>\n"
    else:
        username_string = ""
    if stockSymbol != None:
        stockSymbol_string = "        <stockSymbol>" + stockSymbol + "</stockSymbol>\n"
    else:
        stockSymbol_string = ""
    if filename != None:
        filename_string = "        <filename>" + filename + "</filename>\n"
    else:
        filename_string = ""
    if funds != None:
        funds_string = "        <funds>" + funds + "</funds>\n"
    else:
        funds_string = ""
    return "    <userCommand>\n" + timestamp_string + server_string + transactionNum_string + command_string + username_string + "    </userCommand>\n"

def generate_quoteServer(timestamp, server, transactionNum, price, stockSymbol, username, quoteServerTime, cryptokey):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    price_string = "        <price>" + price + "</price>\n"
    stockSymbol_string = "        <stockSymbol>" + stockSymbol + "</stockSymbol>\n"
    username_string = "        <username>" + username + "</username>\n"
    quoteServerTime_string="        <quoteServerTime>" + quoteServerTime + "</quoteServerTime>\n"
    cryptokey_string="        <cryptokey>" + cryptokey + "</cryptokey>\n"
    return "    <quoteServer>\n" + timestamp_string + server_string + transactionNum_string + price_string + stockSymbol_string + username_string + quoteServerTime_string + cryptokey_string + "    </quoteServer>\n"

def generate_accountTransaction(timestamp, server, transactionNum, action, username, funds):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    action_string = "        <action>" + action + "</action>\n"
    username_string = "        <username>" + username + "</username>\n"
    funds_string = "        <funds>" + funds + "</funds>\n"
    return "    <accountTransaction>\n" + timestamp_string + server_string + transactionNum_string + action_string + username_string + funds_string + "    </accountTransaction>\n"

def generate_systemEvent(timestamp, server, transactionNum, command, username = None, stockSymbol = None, filename = None, funds = None):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    command_string = "        <command>" + command + "</command>\n"
    if stockSymbol != None:
        stockSymbol_string = "        <stockSymbol>" + stockSymbol + "</stockSymbol>\n"
    else:
        stockSymbol_string = ""
    if filename != None:
        filename_string = "        <filename>" + filename + "</filename>\n"
    else:
        filename_string = ""
    if funds != None:
        funds_string = "        <funds>" + funds + "</funds>\n"
    else:
        funds_string = ""
    return "    <systemEvent>\n" + timestamp_string + server_string + transactionNum_string + command_string + stockSymbol_string + filename_string + funds_string + "    </systemEvent>\n"

def generate_errorEvent(timestamp, server, transactionNum, command, username = None, stockSymbol = None, filename = None, funds = None, errorMessage = None):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    command_string = "        <command>" + command + "</command>\n"
    if username != None:
        username_string = "        <username>" + username + "</username>\n"
    else:
        username_string = ""
    if stockSymbol != None:
        stockSymbol_string = "        <stockSymbol>" + stockSymbol + "</stockSymbol>\n"
    else:
        stockSymbol_string = ""
    if filename != None:
        filename_string = "        <filename>" + filename + "</filename>\n"
    else:
        filename_string = ""
    if funds != None:
        funds_string = "        <funds>" + funds + "</funds>\n"
    else:
        funds_string = ""
    if errorMessage != None:
        errorMessage_string = "        <errorMessage>" + errorMessage + "</errorMessage>\n"
    else:
        errorMessage_string = ""

    return "    <errorEvent>\n" + timestamp_string + server_string + transactionNum_string + command_string + username_string + stockSymbol_string + filename_string + funds_string + errorMessage_string + "    </errorEvent>\n"

def generate_debugEvent(timestamp, server, transactionNum, command, username = None, stockSymbol = None, filename = None, funds = None, debugMessage = None):
    timestamp_string = "        <timestamp>" + timestamp + "</timestamp>\n"
    server_string = "        <server>" + server + "</server>\n"
    transactionNum_string = "        <transactionNum>" + transactionNum + "</transactionNum>\n"
    command_string = "        <command>" + command + "</command>\n"
    if username != None:
        username_string = "        <username>" + username + "</username>\n"
    else:
        username_string = ""
    if stockSymbol != None:
        stockSymbol_string = "        <stockSymbol>" + stockSymbol + "</stockSymbol>\n"
    else:
        stockSymbol_string = ""
    if filename != None:
        filename_string = "        <filename>" + filename + "</filename>\n"
    else:
        filename_string = ""
    if funds != None:
        funds_string = "        <funds>" + funds + "</funds>\n"
    else:
        funds_string = ""
    if debugMessage != None:
        debugMessage_string = "        <debugMessage>" + debugMessage + "</debugMessage>\n"
    else:
        debugMessage_string = ""

    return "    <errorEvent>\n" + timestamp_string + server_string + transactionNum_string + command_string + username_string + stockSymbol_string + filename_string + funds_string + debugMessage_string + "    </errorEvent>\n"


def generate_file():
    f = open("logfile.xml", "w")
    f.write("<?xml version=\"1.0\"?>\n")
    f.write("<log>\n")
    f.write(generate_userCommand("1609459210000", "test", "1", "ADD", "testname"))
    f.write(generate_quoteServer("1609459210000", "test", "2", "12", "FAE", "fakeuser", "12", "abc"))
    f.write(generate_accountTransaction("1609459210000", "test", "3", "nothing", "fakeuser", "100"))
    f.write(generate_systemEvent("1609459210000", "test", "4", "BUY", "FAE"))
    f.write(generate_errorEvent("1609459210000", "test", "5", "BUY", "testName"))
    f.write(generate_debugEvent("1609459210000", "test", "5", "BUY", "testName"))
    f.write("</log>\n")
    f.close()

def main():
    print("Generated File")
    generate_file()

if __name__ == "__main__":
    main()