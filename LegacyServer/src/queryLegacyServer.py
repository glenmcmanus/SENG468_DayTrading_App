from subprocess import Popen, PIPE, run

#This code is incomplete
#All it is currently doing is connecting to the legacy server, sending a query, then printing a response
#TODO:
#send any stock and username, not just hardcoded
#reformat ouput in some way
#send output to transaction server (possibly a different file)
proc = Popen(['nc', '192.168.4.2', '4444'], stdin=PIPE, stdout=PIPE)
proc.stdin.write(b"SYM username\r")
output = proc.communicate()[0]
print((output[0:-1].decode("utf-8"))