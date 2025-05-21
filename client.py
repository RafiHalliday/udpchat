# CLIENTSIDE for AnakBuElsa UDP Chat

# *** Set Up Client Socket ***
# Import library
import socket
import threading
import sys

# Welcome messages and initialization
welcomeMessage = '''
----------------------------------------------------------------------------
|               Welcome to AnakBuElsa UDP Chat Application                 |
|                 made by RafiHalliday & M. Arya Putra P.                  |
|                                                                          |
|                this is the client side of the application                |
|                be sure to first INITIALIZE the SERVER SIDE               |
|                                                                          |
|                  please use input your IP Address & Port                 |
|                   and the server's IP Address & Port                     |
|       your IP Address & Port will be used as the client's address        |
|   the server's IP Address & Port will be used as the server's address    |
|                                                                          |
----------------------------------------------------------------------------
'''
print(welcomeMessage)

# Initialize client and server address
clientIP, clientPort = str, int
serverIP, serverPort = str, int

# Input clientIP and clientPort, serverIP and serverPort
clientIP = str(input("Input client IP: "))
clientPort = int(input("Input client Port: "))

serverIP = str(input("Input server IP: "))
serverPort = int(input("Input server Port: "))

# Testing IP and Port
# clientIP = "localhost"
# clientPort = 9000
# serverIP = "localhost"
# serverPort = 8000

# Put IP and Port into respective addresss
serverAddress = (serverIP, serverPort)
clientAddress = (clientIP, clientPort)

# Initialize client's socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(clientAddress)

# Initialize client's status
clientUsername = str
clientChat = str
clientUsername = None
clientChat = None

# Print initialization status
initializationStatus = f'''
Client Address : {clientAddress}
Server Address : {serverAddress}
'''
print(initializationStatus)

# Declare initialization complete
print("Initialization complete!")
print("Please use /help to see the list of commands")



# ------------------------------------------------------------------------------
# *** Send Message ***
# This is PROBABLY the function that will be given TCP later on
# CORRECTION: sendto() function is the function that will be encapsulated in a TCP over UDP implementation

def sendingToServer():
    while True:
        message = input("")
        if message == "!q":
            # exit()
            print("Bye")
            sys.exit()
            client.close()
        elif message in command_list:
            match message:
                case "/help":
                    requestHelp()
                case "/register":
                    requestRegister()
                case "/login":
                    requestLogin()
                case "/createChat":
                    requestCreateChat()
                case "/joinChat":
                    requestJoinChat()
                case "/logout":
                    requestLogout()
                case "/leaveChat":
                    requestLeaveChat()
                case "/status":
                    status()
        else:
            global clientUsername, clientChat
            if clientChat == None: # user is not logged in and not in a chatroom
                echo(message)
            elif clientUsername != None and clientChat != None: #user is logged in and in a chatroom
                sendToChat(message)
            # failsafe if message has no/broken header
            else:
                pass



# ------------------------------------------------------------------------------
# *** Receive Message ***
def receive():
    while True:
        try:
            message, _ = client.recvfrom(2048)
            decodedMessage = message.decode()
            User_Receive_Flag = decodedMessage[:18]
            # DEBUGGING : check decoded message
            # print("---")
            # print(decodedMessage)
            # print("---")

            if User_Receive_Flag == "USER_RECEIVE_FLAG:":
                User_Respond_Info = decodedMessage[18:]
                User_Respond_Number = User_Respond_Info.split(",")[0]
                match User_Respond_Number:
                    case "0":
                        respondHelp(User_Respond_Info)
                    case "1":
                        respondRegister(User_Respond_Info)
                    case "2":
                        respondLogin(User_Respond_Info)
                        # print(f"user: {clientUsername}")
                    case "3":
                        respondCreateChat(User_Respond_Info)
                    case "4":
                        respondJoinChat(User_Respond_Info)
                        # print(f"chat: {clientChat}")
                    case "5":
                        respondLogout(User_Respond_Info)
                    case "6":
                        respondLeaveChat(User_Respond_Info)
                    case "7":
                        respondEcho(User_Respond_Info)
                    case "8":
                        respondSendToChat(User_Respond_Info)

                # Hardcode Status Checker
                # Get current username and chatroom
                # global clientUsername, clientChat
                # print(clientUsername, clientChat)
                # print("-------------------------")

            # failsafe if received message has no/broken header
            else:
                print(decodedMessage)
        except:
            pass



# ------------------------------------------------------------------------------
# *** CLIENT SIDE STATUS CHECKER ***
def status():
    global clientAddress, serverAddress, clientUsername, clientChat
    currentStatus = f'''
---------------------------------------------
    Current Clientside Status               
    clientAddress   : {clientAddress}       
    serverAddress   : {serverAddress}       
    clientUsername  : {clientUsername}      
    clientChat      : {clientChat}          
---------------------------------------------
'''
    print(currentStatus)



# ------------------------------------------------------------------------------
# *** Command/Request for Server ***
command_list = ["/help", "/register", "/login", "/createChat", "/joinChat", "/logout", "/leaveChat", "/status"]
# REQUEST FUNCTIONS
# 0. REQUEST HELP
def requestHelp():
    command_tag = 0
    client.sendto(f"COMMAND_TAG:{command_tag}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag}")

# 1. REQUEST REGISTER
def requestRegister():
    command_tag = 1
    username = str(input("Register username: "))
    global clientUsername

    # check if user is already logged in with the username
    # if yes it means the username is already registered
    if clientUsername == username:
        print(f"You are already logged in and registered as \"{username}\", Please reuse /register with a different username")
    else:
        client.sendto(f"COMMAND_TAG:{command_tag},{username}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{username}")

# 2. REQUEST LOGIN
def requestLogin():
    command_tag = 2
    username = str(input("Username: "))
    global clientUsername

    # Check if user is currently logged in
    if clientUsername != None and clientUsername != None:
        print(f"You are already logged in as \"{clientUsername}\", please logout before logging in")
    else:
        client.sendto(f"COMMAND_TAG:{command_tag},{username}".encode(), serverAddress) 

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{username}")

# 3. REQUEST CREATE CHAT
def requestCreateChat():
    command_tag = 3
    chatName = str(input("Chatname: "))
    global clientChat
    # Check if user is currently in a chatroom
    # if yes it means the chatroom has already been created
    if chatName == clientChat:
        print("This chatroom has already been created and you are in it!")
    else:
        chatPass = str(input("Chat password: "))
        client.sendto(f"COMMAND_TAG:{command_tag},{chatName},{chatPass}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{chatName},{chatPass}")

# 4. REQUEST JOIN CHAT
def requestJoinChat():
    command_tag = 4

    global clientUsername, clientChat

    joiningUsername = clientUsername

    # Check if user is logged in
    # user cannot join a chatroom unless logged in
    if joiningUsername == None:
        print(f"You are not logged in! Please log in before joining a chatroom")
    # Check if clientChat is empty and if user has already joined a chatroom
    # if clienChat is empty then user can join a chatroom
    elif clientChat != None:
        print(f"You have already joined the chatroom \"{clientChat}\", please leave any chat before using /joinChat")
    else:
        joiningChatname = str(input("Chatname: "))
        joiningPass = str(input("Chat password: "))
        client.sendto(f"COMMAND_TAG:{command_tag},{joiningUsername},{joiningChatname},{joiningPass}".encode(), serverAddress) 

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{joiningUsername},{joiningChatname},{joiningPass}")

# 5. REQUEST LOGOUT
def requestLogout():
    command_tag = 5

    global clientUsername, clientChat
    username = clientUsername
    chat = clientChat
    if username == None:
        print("You are already logged out")
    else:
        client.sendto(f"COMMAND_TAG:{command_tag},{username},{chat}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{username},{chat}")

# 6. REQUEST LEAVE CHAT
def requestLeaveChat():
    command_tag = 6

    global clientUsername, clientChat

    if clientChat == None:
        print("You have already left chatroom")
    else:
        client.sendto(f"COMMAND_TAG:{command_tag},{clientUsername},{clientChat}".encode(), (serverAddress))

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{clientUsername},{clientChat}")

# 7. ECHO
def echo(message):
    command_tag = 7

    global clientUsername
    echoUsername = clientUsername
    client.sendto(f"COMMAND_TAG:{command_tag},{message},{echoUsername}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{message},{echoUsername}")

# 8. SEND TO CHAT
def sendToChat(message):
    command_tag = 8

    global clientUsername
    global clientChat
    client.sendto(f"COMMAND_TAG:{command_tag},{message},{clientUsername},{clientChat}".encode(), serverAddress)

    # DEBUGGING : check command info being sent
    # print(f"COMMAND_TAG:{command_tag},{message},{clientUsername},{clientChat}")



# ------------------------------------------------------------------------------
# *** Reacting to Response from Server ***
# 0. HELP
def respondHelp(User_Respond_Info):
    # Help Message
    helpMessage = '''
---------------------------------------------------------------------  
|    LIST OF COMMANDS:                                              |
|    1.  /help       : see list of commands                         |
|    2.  /register   : register a new account                       |
|    3.  /login      : log into existing accounts                   |
|    4.  /createChat : create a new chatroom                        |
|    5.  /joinChat   : join existing chatrooms                      |
|    6.  /logout     : log out from current user                    |
|    7.  /leaveChat  : leave current chatroom                       |
|    8.  /status     : check current address, username, and chat    |
---------------------------------------------------------------------
    '''
    print(helpMessage)
    
    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 1. REGISTER
def respondRegister(User_Respond_Info):
    usernameAvailable = User_Respond_Info.split(",")[1]
    username = User_Respond_Info.split(",")[2]

    if usernameAvailable == "True":
        print(f"Succesfully registered username \"{username}\"!")
        print("Please log in using the username")

    else:
        print(f"Username \"{username}\" is not available!")
        print("Please reuse /register with a different username")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 2. LOGIN
def respondLogin(User_Respond_Info):
    usernameUsable = User_Respond_Info.split(",")[1]
    username = User_Respond_Info.split(",")[2]
    global clientUsername

    if usernameUsable == "True":
        print(f"Logged in successfully using username \"{username}\"!")
        clientUsername = username
        
    else:
        print(f"Username \"{username}\" does not exist!")
        print("Please reuse /login with existing username")

    print(f"Current username: {clientUsername}")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 3. CREATE CHATROOM
def respondCreateChat(User_Respond_Info):
    chatroomAvailable = User_Respond_Info.split(",")[1]
    chatName = User_Respond_Info.split(",")[2]
    chatPass = User_Respond_Info.split(",")[3]
    if chatroomAvailable == "True":
        print(f"Chatroom created! Please join the chatroom \"{chatName}\" using the password \"{chatPass}\"")
    else:
        print(f"Chatname \"{chatName}\" is already taken! Please reuse /createChat with a different chatname")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 4. JOIN CHATROOM
def respondJoinChat(User_Respond_Info):
    chatExists = User_Respond_Info.split(",")[1]
    passwordCorrect = User_Respond_Info.split(",")[2]
    joiningChatname = User_Respond_Info.split(",")[3]
    joiningPass = User_Respond_Info.split(",")[4]

    global clientChat

    if chatExists == "True":
        if passwordCorrect == "True":
            clientChat = joiningChatname
            print(f"Current chat: {clientChat}")
        else:
            clientChat = None
            print(f"Password \"{joiningPass}\" is incorrect! Please reuse /joinchat with a correct password for chat \"{joiningChatname}\"")
    else:
        clientChat = None
        print(f"Chat \"{joiningChatname}\" does not exist! Please reuse /joinChat with existing chatName")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 5. LOGOUT
def respondLogout(User_Respond_Info):
    username = User_Respond_Info.split(",")[1]
    # unused but maybe useful
    # chat = User_Respond_Info.split(",")[2]

    global clientUsername, clientChat

    print(f"Successfully logged out from user \"{username}\"")
    clientUsername = None

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 6. LEAVE CHAT
def respondLeaveChat(User_Respond_Info):
    # unused but maybe useful
    # username = User_Respond_Info.split(",")[1]
    chat = User_Respond_Info.split(",")[2]

    global clientChat
    clientChat = None
    print(f"Successfully left chatroom \"{chat}\"")
    
    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 7. ECHO
def respondEcho(User_Respond_Info):
    echoUsername = User_Respond_Info.split(",")[1]
    echoMessage = User_Respond_Info.split(",")[2]

    if echoUsername != "None":
        print(f"{echoUsername} ECHO: {echoMessage}")
    else:
        print(f"SERVER ECHO: {echoMessage}")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)

# 8. SEND TO CHAT
def respondSendToChat(User_Respond_Info):
    # get message, clientUsername, clientChat
    message = User_Respond_Info.split(",")[1]
    clientUsername = User_Respond_Info.split(",")[2]
    clientChat = User_Respond_Info.split(",")[3]

    print(f"{clientChat} | {clientUsername}: {message}")

    # DEBUGGING : print User_Respond_Info
    # print(User_Respond_Info)



# ------------------------------------------------------------------------------
# *** Running Clientside ***
# THREADING
tReceiving = threading.Thread(target=receive)
tReceiving.start()

tSending = threading.Thread(target=sendingToServer)
tSending.start()

# END OF CODE
