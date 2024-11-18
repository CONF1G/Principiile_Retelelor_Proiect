import socket
import threading
import random

# Configurări
TCP_IP = '0.0.0.0'
TCP_PORT = 12345
UDP_PORT = 12346

clients = {}


# Funcție pentru gestionarea unui client TCP
def handle_client(client_socket, client_address):
    print(f"[CONEXIUNE] Client conectat: {client_address}")

    # Verifică dacă clientul a mai jucat înainte, altfel generează un număr secret nou
    if client_address not in clients:
        secret_number = random.randint(1, 100)
        clients[client_address] = secret_number
    else:
        secret_number = clients[client_address]

    client_socket.send("Bun venit la 'Guess the Number'! Ghiceste un numar intre 1 si 100.\n".encode())

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            try:
                guess = int(data.strip())
                if guess < secret_number:
                    response = "Prea mic!"
                elif guess > secret_number:
                    response = "Prea mare!"
                else:
                    response = "Felicitari! Ai ghicit!"
                    client_socket.send(response.encode())
                    break
            except ValueError:
                response = "Te rog introdu un numar valid."

            client_socket.send(response.encode())
        except Exception as e:
            print(f"[EROARE] {e}")
            break

    client_socket.close()
    print(f"[DECONEXIUNE] Client deconectat: {client_address}")


# Funcție pentru gestionarea unui client UDP
def handle_udp_client(message, client_address, udp_socket):
    print(f"[UDP] Mesaj primit de la {client_address}: {message.decode()}")

    # Verifică dacă clientul a mai jucat înainte, altfel generează un număr secret nou
    if client_address not in clients:
        secret_number = random.randint(1, 100)
        clients[client_address] = secret_number
    else:
        secret_number = clients[client_address]

    try:
        # Procesarea ghicirii
        try:
            guess = int(message.decode().strip())
            if guess < secret_number:
                response = "Prea mic!"
            elif guess > secret_number:
                response = "Prea mare!"
            else:
                response = "Felicitari! Ai ghicit!"
        except ValueError:
            response = "Te rog introdu un numar valid."

        # Trimiterea răspunsului înapoi clientului
        udp_socket.sendto(response.encode(), client_address)
    except Exception as e:
        print(f"[EROARE UDP] {e}")


# Server TCP
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_PORT))
    server.listen(5)
    print(f"[START] Server TCP rulează pe {TCP_IP}:{TCP_PORT}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


# Server UDP
def udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((TCP_IP, UDP_PORT))
    print(f"[START] Server UDP rulează pe {TCP_IP}:{UDP_PORT}")

    while True:
        try:
            # Așteaptă să primească un mesaj de la un client
            message, client_address = udp_socket.recvfrom(1024)
            print(f"[UDP] Mesaj primit de la {client_address}: {message.decode()}")

            # Creare fir pentru fiecare client care trimite un mesaj
            # Aici pasăm mesajul, adresa clientului și socketul UDP
            client_thread = threading.Thread(target=handle_udp_client, args=(message, client_address, udp_socket))
            client_thread.start()
        except Exception as e:
            print(f"[EROARE GENERALĂ UDP] {e}")


# Pornirea serverelor
if __name__ == "__main__":
    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread = threading.Thread(target=udp_server)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()
