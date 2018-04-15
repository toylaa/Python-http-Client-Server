# @author Tyler McDonough 
# @tcmcd1337@gmail.com
## cps530_01
### http_server.py


# Import socket module
from socket import *    

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#Get from user a port number, and assign to the socket

print ("\n\n------------------------------------------------------------------------")
print ("			[_TcMpYtHoN_Server_2.0_]")
print ("------------------------------------------------------------------------")
serverPort = input("Please Enter a port number: ")
serverPort = int(serverPort)

# Bind the socket to server address and server port
serverSocket.bind(("",serverPort))

# Start listening to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print ("\n>Ready to Serve... ")
	# Set up a new connection from the client    
	connectionSocket,addr = serverSocket.accept()
	
	# If an exception occurs during the execution of try block
	# the rest of the block is skipped
	# If the exception type matches the word after "except" statement
	# the except clause is executed
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1024)

                # You can print this message to see how an http request looks like.
                # Request format is specified in the http RFC
                # Write code to print incoming http request

		print ("\n>Recieved message from client: \n" + message + "\n")
		
		# Kill server logic
		if message.lower()=='kill':
			print ("...\n..\n.\n\n'No, no, It's uh,...just resting.")
			connectionSocket.close()
			break
		
		# Extract the path of the requested file from the message
        # If you split the message into tokens, the filename will be the second token
		# The path is the second part of HTTP header, identified by index [1]
                                
		filename = message.split()[1]
		print ("\n>Requested file name: " + filename	)
                
		# get rid of the leading '/'
		filename = filename[1:]		

        # Store the entire content of the requested file in a temporary buffer				
		file = open( filename  , "r")
		outputdata = file.read()
		print ("Contents: \n" + outputdata)
		print ("------------------------------------------------------------------------")

        # Send the HTTP response header line to the connection socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
 
		# Send the content of the requested file to the connection socket                
		connectionSocket.send(outputdata)
		print ("\n\nSent: \n" + outputdata)
		
		# Close the client connection socket                
		connectionSocket.close()
		print ("------------------------------------------------------------------------")
                
	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
		connectionSocket.send("<html><head></head><body><h1>404 Not Found - Please Check your filename!</h1></body></html>\r\n")
		print ("\n>>File Not Found Error 404: Http Response sent:")
		print ("HTTP/1.1 404 Not Found\r\n\r\n" )
		print ("------------------------------------------------------------------------")		
	# Close the client connection socket		
	connectionSocket.close()
		
# close the server socket
serverSocket.close()
                


