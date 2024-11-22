import socket

HOST = "0.0.0.0"
PORT = 5005  # Cổng nhận dữ liệu từ điện thoại
ESP_PORT = 5006  # Cổng để gửi dữ liệu tới ESP

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server đang lắng nghe tại {HOST}:{PORT}...")

        # Thiết lập một socket thứ hai để gửi dữ liệu đến ESP qua cổng 5006
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as esp_socket:
            esp_socket.bind((HOST, ESP_PORT))
            esp_socket.listen()
            print(f"Server đang lắng nghe tại {HOST}:{ESP_PORT} cho ESP...")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Kết nối từ điện thoại tại {client_address}")

                esp_conn, esp_address = esp_socket.accept()
                print(f"Kết nối từ ESP tại {esp_address}")

                with client_socket, esp_conn:
                    while True:
                        try:
                            # Nhận dữ liệu từ điện thoại
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            
                            # In lệnh nhận được từ điện thoại
                            script = data.decode('utf-8').replace('\n', '\0')
                            print(f"Lệnh nhận được từ điện thoại: {script}")
                            client_socket.sendall(b"da nhan")

                            # Gửi dữ liệu tới ESP qua cổng 50060
                            try:
                                esp_conn.sendall(script.encode('utf-8'))
                                print("Dữ liệu đã gửi tới ESP")
                            except ConnectionResetError:
                                print("Lỗi: Kết nối tới ESP đã bị đóng.")
                                break  # Exit the loop if the connection is lost
                            
                        except socket.timeout:
                            print("Lỗi: Kết nối đã hết thời gian chờ.")
                            break
                        except UnicodeDecodeError:
                            print("Lỗi giải mã dữ liệu. Dữ liệu không phải là chuỗi UTF-8.")
                            continue

tcp_server()
