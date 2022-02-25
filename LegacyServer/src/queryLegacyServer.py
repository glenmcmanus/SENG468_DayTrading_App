git from subprocess import Popen, PIPE, run

#This code is incomplete

#TODO:
#receive input from transaction server
#reformat ouput in some way
#send output to transaction server (possibly a different file)

def query_server(stock_symbol, username):
    proc = Popen(['nc 192.168.4.2 4444'], stdin=PIPE, stdout=PIPE, shell=True)
    proc.stdin.write(("" + stock_symbol + " " + username + "\r").encode("utf-8"))
    output = proc.communicate()[0]
    return output.decode("utf-8")

def process_request(stock_symbol, username):
    query_string = query_server(stock_symbol, username)
    return query_string.split(",")

def main():
    stock_info = process_request("TES", "fakeUser")
    print(stock_info)
    print(stock_info[0])
    print(stock_info[1])
    print(stock_info[2])
    print(stock_info[3])
    print(stock_info[4])

if __name__ == "__main__":
    main()
