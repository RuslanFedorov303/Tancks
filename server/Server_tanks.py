from Classes import *


HOST = 'localhost'
IP = 8081


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, IP))
server_socket.listen(5)

players = []


def receivingData():
    information_received = player_socket.recv(1024).decode().strip()
    information_received = json.loads(information_received)
    information_received[0] = pygame.event.Event(information_received["type"], information_received)
    return information_received


def sendingData(information_received, player_socket):
    information_for_sending = json.dumps(information_received)
    for player in players:
        player.send(information_for_sending.encode())


# def userConnect():
#     pass


def playerUpdate(player_socket):
    tank = Tank(body_image       = body_image,
                turret_image     = turret_image,
                gun_image        = gun_image,
                projectile_image = projectile_image)
    while True:
        try:
            tank.tankUpdate(receivingData())
            sendingData(tank.get_data())


        except Exception as ex:
            print(ex)




while True:
    player_socket, addr = server_socket.accept()
    players.append(player_socket)
    threading.Thread(target=playerUpdate, args=(player_socket,), daemon=True).start()