import json

from Classes import *


HOST = '0.0.0.0'
IP = 8081


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, IP))
server_socket.listen(5)

players = []


def receivingData(player_socket):
    information_received = player_socket.recv(1024).decode().strip()
    information_received = json.loads(information_received)
    return information_received


def sendingData(player):
    data_players = list()

    for player_data in players:
        data_players.append(
            player_data['tank'].getData()
        )

    player['socket'].send(
            json.dumps(
                data_players
            ).encode()
    )



def playerUpdate(player):
    while True:
        try:
            event = receivingData(player['socket'])

            player['tank'].tankUpdate(
                event[0], event[1], event[2]
            )

            sendingData(player)


        except Exception as ex:
            print(ex)

        print(player['tank'].getData())



while True:
    player_socket, addr = server_socket.accept()
    players.append(
        {
            'ID'    : len(players) + 1,
            'socket': player_socket,
            'tank'  : Tank(
                body_image=body_image,
                turret_image=turret_image,
                gun_image=gun_image,
                projectile_image=projectile_image,
                player_ID = len(players) + 1,
                x_coord=500 + len(players) * 100, y_coord=500
            )
        }
    )
    threading.Thread(target=playerUpdate,
                     args=(players[-1],),
                     daemon=True).start()