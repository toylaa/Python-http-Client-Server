# @author Tyler McDonough 
# @tcmcd1337@gmail.com
## cps530_01
### http_client.py
#####################

# Import socket module
from socket import *	

#initialize loop control variable
first = True			

while True:
	
	#logic for first iteration
	if first:
		print ("\n\n------------------------------------------------------------------------")
		print ("			[_TcMpYtHoN_Client_2.0_]")
		print ("------------------------------------------------------------------------")
		serverName=input(">Please enter Server Name/IP: ")
		serverPort=int(input(">Please enter Server Port #: "))
		fileName = input(">Which File to get from server: ")
		fileToWrite = input(">Local file to write data from server: ")
		
		# Command option control variable
		# After first iteration provide user with options to re-use connection
	
	#logic for subsequent iterations
	if first == False:
		print (""" 
		\n\n------------------------------------------------------------------------
		
->> To Continue, please enter a new Server Name/IP...	
	**OR**
>Enter a client command: 
	--> 'same' --- Reconnect to same server and port
	--> 'end'  --- Shutdown Client	
	--> 'kill' --- Shutdown Server"""		)
				
		options=input("-->:")		#Prompt for IP address/client options
		
		#shutdown client when 'end' is entered 
		if options.lower() == 'end':
			break
		#shutdown SERVER remotely when 'kill' is entered
		if options.lower() == 'kill':		
			clientSocket = socket(AF_INET, SOCK_STREAM)
			clientSocket.connect((serverName, serverPort))
			clientSocket.send('kill')		
			print (" \n..The plumage don't enter into it. It's stone dead. ")
			break
		
		# retain IP and port info when 'same' is entered
		if options.lower() == 'same':
			print (">>Connection to Server @ ["+ serverName + ":" + str(serverPort) + "] reinstantiated")
		
		#only require additional port # when creating new connection 
		else:
			serverPort=int(input(">Please enter Server Port #: "))
		
		fileName  = input(">Which File to get from server: ")
		fileToWrite=input(">Local file to write data from server: ")

	# Create a TCP server socket, connect it to the port # given
		
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	
	# compose an http request header for a GET request
	requestMessage = "GET /"+fileName + " HTTP/1.1 \r\n" + "User-agent: Python \r\nFrom: toylaa@aol.com"

	requestMessage.encode("utf-8")
	clientSocket.send(requestMessage)		# Send the request through the socket	
	
	
	
	# Receive the bytes from the socket
	requestResult =clientSocket.recv(1024)	
	print ("\n>>> " + requestResult)
	
	serverReturn = clientSocket.recv(1024)	## receive actual file contents
	
	# if incoming data has length 0, print to console; break.
	if len(serverReturn) == 0:
		print ("Server File Found :  '" + fileName + "'\n")
		print ("**Incoming data from file has length zer0..-->**BREAK**")
		break
			
	# parse http header response - if NOT 404 -- file found logic
	if requestResult.split()[1] != '404':		
		try:
			# Open the local file to which incoming data (server's response)  is to be written. 
			file = open( fileToWrite  , "w")
			
		except IOError:		#catch IOErrors
			print("Could not open/Create file. No valid destination filename entered.")
			break  
			
		# write to console.
		print ("\n>>Contents returned from server: '" + fileName +"'\n"+ serverReturn 	)
		print ("\n\n>> Written to file --> ' " + fileToWrite	+ " '")
		
		file.write(str(serverReturn))	# write to file.		
		file.close	# Close(/save) the opened local file.
	
	# parse http header response - if 404 -- file NOT found logic
	elif int(requestResult.split()[1])==404: 
		print ("....Requested file '" + fileName + "' not found on server. ")
		print ("		-Please try again.")
	
	# loop option control - mark 'first' as false after first iteration
	if first == True:
		first = False		
						
	clientSocket.close 				# Close the socket connection
