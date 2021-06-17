from _thread import start_new_thread
from socket import *
from tkinter import *
from threading import *
from tkinter.scrolledtext import ScrolledText


class TCP_ChatServer:
    list_clients = []   # 소켓을 담을 리스트
    server_socket = None

    def __init__(self):
        self.set_gui()  # GUI 생성 메서드

    def set_gui(self):
        self.r = Tk()
        self.r.title('채팅 프로그램 (Server)')
        self.r.geometry('500x600')

        self.l_title = Label(self.r, text='------------------------------------- Chat Server -------------------------------------')
        self.l_title.place(x=20, y=0)

        self.l_explanation = Label(self.r, text='※  열고자 하는 서버의 IP와 Port 번호를 입력해주세요.')
        self.l_explanation.place(x=20, y=25)

        self.l_IP = Label(self.r, text='Server IP : ')
        self.l_IP.place(x=19, y=55)

        self.e_IP = Entry(self.r, width=10, text='127.0.0.1')
        self.e_IP.place(x=82, y=57)
        self.e_IP.insert(0, '127.0.0.1')

        self.l_Port = Label(self.r, text='Port : ')
        self.l_Port.place(x=180, y=55)

        self.e_Port = Entry(self.r, width=6, text='2500')
        self.e_Port.place(x=218, y=57)
        self.e_Port.insert(0, '2500')

        self.b_Open = Button(self.r, text='서버 열기', command=self.open_server)
        self.b_Open.place(x=290, y=53)

        self.b_Close = Button(self.r, text='서버 닫기', command=exit)
        self.b_Close.place(x=390, y=53)

        self.l_Log = Label(self.r, text='Log')
        self.l_Log.place(x=20, y=83)

        self.t_Log_area = ScrolledText(self.r, height=35, width=64)
        self.t_Log_area.place(x=20, y=108)

    def open_server(self):       # 서버 열기
        IP = self.e_IP.get()
        PORT = int(self.e_Port.get())
        self.b_Open['state'] = 'disabled'
        self.e_IP['state'] = 'readonly'
        self.e_Port['state'] = 'readonly'
        start_new_thread(self.make_socket, (IP, PORT))

    def make_socket(self, IP, PORT):        # 소켓 생성, 바인드, 리스닝 및 수락
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 소켓 옵션 설정
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen()
        fp = open('Server Log.txt', 'a')
        self.t_Log_area.insert("end", '\n====================== 서버가 열렸습니다 ======================\n\n')
        fp.write('\n====================== 서버가 열렸습니다 ======================\n\n')
        self.t_Log_area.insert("end", '클라이언트의 입장을 기다리고 있습니다.\n')
        fp.write('클라이언트의 입장을 기다리고 있습니다.\n')

        while True:
            fp = open('Server Log.txt', 'a')
            client_socket, addr = self.server_socket.accept()  # accept()을 통해 연결 수락
            if client_socket not in self.list_clients:      # 해당 소켓을 리스트에 삽입
                self.list_clients.append(client_socket)

            self.t_Log_area.insert("end", '[Connected] IP:{0} / Port:{1}가 연결되었습니다.\n'.format(addr[0], str(addr[1])))
            fp.write('[Connected] IP:{0} / Port:{1}가 연결되었습니다.\n'.format(addr[0], str(addr[1])))
            self.t_Log_area.yview(END)
            Thread(target=self.send_recv, args=(client_socket, addr)).start()  # 스레드 생성

    def send_recv(self, client_socket, addr):   # 메시지 전송과 수신
        for client in self.list_clients:
            client.sendall('[알림] {0} 님이 접속하였습니다.'.format(str(addr[1])).encode())    # 알림문 전송
            self.t_Log_area.yview(END)

        while True:
            try:
                fp = open('Server Log.txt', 'a')
                message = client_socket.recv(1024)
                self.t_Log_area.insert("end",'[Message Log] ({0}) - {1}  \n'.format(str(addr[1]), str(message.decode())))
                fp.write('[Message Log] ({0}) - {1}  \n'.format(str(addr[1]), str(message.decode())))
                self.t_Log_area.yview(END)
                for client in self.list_clients:
                    client.sendall(message.decode().encode())   # 메시지 전송
            except ConnectionResetError as e:
                fp = open('Server Log.txt', 'a')
                self.list_clients.remove(client_socket)     # 소켓 삭제
                for client in self.list_clients:
                    client.sendall('[알림] {0} 님이 나갔습니다.'.format(str(addr[1])).encode())  # 알림문 전송
                    self.t_Log_area.yview(END)
                self.t_Log_area.insert("end", '[Disconnected] IP:{0} / Port:{1}가 종료되었습니다.\n'.format(addr[0], str(addr[1])))
                fp.write('[Disconnected] IP:{0} / Port:{1}가 종료되었습니다.\n'.format(addr[0], str(addr[1])))
                self.t_Log_area.yview(END)
                break
        client_socket.close()


if __name__ == "__main__":
    TCP_ChatServer()
    mainloop()