# SERVERSIDE for AnakBuElsa UDP Chat

# *** Set Up Server Socket ***
# Import library
import socket
import threading
import queue

print("SERVER_ALERT:STARTING_SERVER")

# Input serverIP and serverPort
serverIP, serverPort = str, int

# Initialization Message
initializationMessage = '''
---------------------------------------------------------------------------------
|               Welcome to AnakBuElsa UDP Chat Application                      |
|                 made by RafiHalliday & M. Arya Putra P.                       |
|                                                                               |
|                this is the server side of the application                     |
|                                                                               |
|             please use input the server's IP Address & Port                   |
|   the server's IP Address & Port will be used as the server's address         |
|                                                                               |
---------------------------------------------------------------------------------
'''

# Comment the code when testing
# Input server IP and Port
serverIP = str(input("Input server IP address: "))
serverPort = int(input("Input server Port: "))

# Testing IP and Port
# clientIP = "localhost"
# serverIP = "localhost"
# clientPort = 9000
# serverPort = 8000

# Put IP and Port into respective addresss
serverAddress = (serverIP, serverPort)

# Print initialization status
initializationStatus = f'''
Server Address : {serverAddress}
'''
print(initializationStatus)

# DATA STRUCTURE & STORAGE
# USERS
users = []

# CHATROOM
chatrooms = []
class Chatroom:
    def __init__(self, chatName, chatPass, chatParticipants):
        self.chatName = chatName
        self.chatPass = chatPass
        self.chatParticipants = chatParticipants
        # TO DO: 
        # ADD chatParticipant ---> DONE
        # server will broadcast a message from a chatparticipant to all other chat participants


# Alert server that it is initializing
print("SERVER_ALERT:INITIALIZING_SERVER")

# Initialize server's socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((serverIP, serverPort))



# ------------------------------------------------------------------------------
# *** Receive Message for Server ***
messages = queue.Queue()

def receive():
    while True:
        try:
            message, addr = server.recvfrom(2048)
            messages.put((message, addr))
        except:
            pass



# ------------------------------------------------------------------------------
#  *** Send Message Back To Client***
def sendToClient():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decodedMessage = message.decode()
            # Print the incoming message on the serverside
            print(decodedMessage)
            client = addr

            # Get users and chatrooms (for when hardcode debug is necessary)
            global users, chatrooms

            # Test length of decoded message (maybe used later)
            # print(len(decodedMessage))

            command_tag = decodedMessage[:12]

            if command_tag == "COMMAND_TAG:":
                command_info = decodedMessage[12:]
                command_number = command_info.split(",")[0]

                match command_number:
                    case "0": # "/help"
                        commandHelp(client)
                    case "1": # "/register"
                        commandRegister(client, command_info)
                    case "2": # "/login"
                        commandLogin(client, command_info)
                    case "3" : # "/createChat"
                        commandCreateChat(client, command_info)
                    case "4" : # "/joinChat":
                        commandJoinChat(client, command_info)
                    case "5":
                        commandLogout(client, command_info)
                    case "6":
                        commandLeaveChat(client, command_info)
                    case "7":
                        commandEcho(client, command_info)
                    case "8":
                        commandSendToChat(client, command_info)
            else:
                # failsafe if message does not correspond with any command
                # send the message back to sender (return to sender)
                server.sendto(message, client)
            
            serverStatus()



# ------------------------------------------------------------------------------
# *** Print Current Serverside Status ***
def serverStatus():
    global users, chatrooms
    # Print current users and chatrooms
    print("")
    print("------------------------------------------------------------------")
    print("Current Serverside Status")
    print(f"Current users:{users}")
    print(f"Current chatroom:{chatrooms}")
    printChatroom()
    print("------------------------------------------------------------------")
    print("")
    return


def printChatroom():
    global chatrooms
    for chatroom in chatrooms:
        print(chatroom.chatName)
        print(chatroom.chatPass)
        print(chatroom.chatParticipants)
        print("")
    return



# ------------------------------------------------------------------------------
# *** Respond to Client Command ***
# List of command_number:
# 0 : client is requesting help (list of commands)
# 1 : client is requesting to register a user
# 2 : client is requesting to login as a user
# 3 : client is requesting to create a new chatroom
# 4 : client is requesting to join a chatroom
# 5 : client is requesting to logout
# 6 : client is requesting to leave a chatroom
# 7 : client has not joined a chatroom, echo all message (return to sender regardless of login status)
# 8 : client is logged in as a user and has joined a chatroom, broadcast all message to appropriate chatroom

# Command 0: HELP
def commandHelp(client):
    # Testing Command Info
    # server.sendto(f"{command_info}".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 0
    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}".encode(), client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag}")
    return

# Command 1: CREATE NEW ACCOUNT
def commandRegister(client, command_info):
    # TESTING MESSAGE
    # server.sendto("REGISTER".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 1
    
    # Get username from client
    username = command_info.split(",")[1]
    # Check if username is unique
    # if username is not unique request another username
    # if username is unique append username to users
    global users
    unique = (username not in users)

    if unique:
        # append username to users
        users.append(username)
        # print server alert
        print(f"SERVER_ALERT:USERS_UPDATED,users={users}")
        usernameAvailable = True

    else:
        usernameAvailable = False
    
    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{usernameAvailable},{username}".encode(), client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{usernameAvailable},{username}")
    return 

# Command 2: LOG INTO ACCOUNT
def commandLogin(client, command_info):
    # TESTING MESSAGE
    # server.sendto("LOGIN".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 2

    # Get username in client
    username = command_info.split(",")[1]

    # Check if username is in users
    global users
    usernameExists = username in users

    # If yes tell client they can log in with that name
    if usernameExists:
        usernameUsable = True
        print(f"SERVER_ALERT:USER_LOGIN,client{client} logged in using username \"{username}\"")
        server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{usernameUsable},{username}".encode(), client)
    # If no tell client they have to log in with a different username
    else:
        usernameUsable = False
        server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{usernameUsable},{username}".encode(), client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{usernameUsable},{username}")
    return

# Command 3: CREATE NEW CHATROOM
def commandCreateChat(client, command_info):
    # TESTING MESSAGE
    # server.sendto("CREATE CHAT".encode(), client)
    
    # set User_Receive_Flag
    User_Receive_Flag = 3 

    # Get chatname from client
    chatName = command_info.split(",")[1]
    # Get chatPass from client
    chatPass = command_info.split(",")[2]

    # check if chatroom is unique
    global chatrooms
    chatUnique = True
    for chatroom in chatrooms:
        if chatName in chatroom.chatName:
            chatUnique = False

    # if chatName is unique, append the chatroom to chatrooms
    if chatUnique:
        # append the new chatroom to chatrooms
        chatrooms.append(Chatroom(chatName, chatPass, []))
        chatroomAvailable = True
        print(f"SERVER_ALERT:NEW_CHATROOM,chatrooms={chatrooms}")
    # if chatName is not unique, send notification to client requesting different chatName
    else:
        chatroomAvailable = False

    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{chatroomAvailable},{chatName},{chatPass}".encode(),client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{chatroomAvailable},{chatName},{chatPass}")
    return

# Command 4: JOIN CHATROOM
def commandJoinChat(client, command_info):
    # TESTING MESSAGE
    # server.sendto("JOIN CHAT".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 4
    joiningUsername = command_info.split(",")[1]
    joiningChatname = command_info.split(",")[2]
    joiningPass = command_info.split(",")[3]

    # check if chatname exists
    global chatrooms
    chatExists = False
    passwordCorrect = False
    for chatroom in chatrooms:
        if chatroom.chatName == joiningChatname:
        # if chatname exists check if password is correct
            chatExists = True
            if chatroom.chatPass == joiningPass:
                # if password is correct client will be added as a chat participant
                passwordCorrect = True
                chatroom.chatParticipants.append(client)

    # put user into said chat
    
    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{chatExists},{passwordCorrect},{joiningChatname},{joiningPass}".encode(), client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{chatExists},{passwordCorrect},{joiningChatname},{joiningPass}")
    return

# Command 5: LOGOUT
def commandLogout(client, command_info):
    # TESTING MESSAGE
    # server.sendto("LOGOUT".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 5

    username = command_info.split(",")[1]
    chat = command_info.split(",")[2]
    global chatrooms

    # If user is in a chatroom user will be removed from chatroom
    if chat != None:
        commandLeaveChat(client, command_info)
    
    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{username},{chat}".encode(),client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{username},{chat}")
    return

# Command 6: LEAVE CHATROOM
def commandLeaveChat(client, command_info):
    # TESTING MESSAGE
    # server.sendto("LEAVE CHAT".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 6

    username = command_info.split(",")[1]
    chat = command_info.split(",")[2]
    global chatrooms

    for chatroom in chatrooms:
        # Remove client from chatroom
        if chatroom.chatName == chat:
            chatroom.chatParticipants.remove(client)
            # Alert server that client was removed from chatroom
            print(f"SERVER_ALERT:REMOVE_CLIENT_FROM_CHAT,user:{username} from client:{client} was removed from chatroom:{chat}")
            # Alert the chat that client was removed from chatroom
            # use SEND TO CHAT function

    # Alert client that it has been removed from chatroom
    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{username},{chat}".encode(),client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{username},{chat}")
    return

# Command 7: ECHO
def commandEcho(client, command_info):
    # TESTING MESSAGE
    # server.sendto("ECHO".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 7

    echoMessage = command_info.split(",")[1]
    echoUsername = command_info.split(",")[2]
    print(f"SERVER_ALERT:ECHO,user:{echoUsername},message:{echoMessage}")
    print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{echoUsername},{echoMessage}")

    server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{echoUsername},{echoMessage}".encode(), client)

    # DEBUGGING : print User_Receive_Info being sent
    # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{echoUsername},{echoMessage}")
    return

# Command 8: SEND TO CHAT
def commandSendToChat(client, command_info):
    # TESTING MESSAGE
    # server.sendto("SEND TO CHAT".encode(), client)

    # set User_Receive_Flag
    User_Receive_Flag = 8

    # get message, clientUsername, clientChat
    message = command_info.split(",")[1]
    clientUsername = command_info.split(",")[2]
    clientChat = command_info.split(",")[3]

    global chatrooms
    # get corresponding chatroom and send message to all participants in the chatroom
    for chatroom in chatrooms:
        if chatroom.chatName == clientChat:
            for participant in chatroom.chatParticipants:
                server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{message},{clientUsername},{clientChat}".encode(), participant)
                print(f"{clientChat} | {clientUsername}: {message}")

    # DEBUGGING : print User_Receive_Info being sent
    print(f"USER_RECEIVE_FLAG:{User_Receive_Flag},{message},{clientUsername},{clientChat}")
    return


# ------------------------------------------------------------------------------
# *** Running Serverside ***
# THREADING
tReceive = threading.Thread(target=receive)
tSendToClient = threading.Thread(target=sendToClient)

tReceive.start()
tSendToClient.start()

# END OF CODE
