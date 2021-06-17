from socket import *
from time import sleep
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *


class TCP_ChatClient:
    client_socket = None
    T_F_Discon = False
    T_F_send = False

    def __init__(self):
        self.set_gui()  # GUI 생성 메서드

    def set_gui(self):
        self.r = Tk()        # Tk 객체 생성
        self.r.title('채팅 프로그램 (Client)')
        self.r.geometry('500x560')

        self.l_title = Label(self.r, text='-------------------------------------- Chat Client --------------------------------------')
        self.l_title.place(x=20, y=0)

        self.l_explanation = Label(self.r, text='※  접속하고자 하는 서버의 IP와 Port 번호를 입력해주세요.')
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

        self.b_Connect = Button(self.r, text='연결 요청', command=self.connect_server)
        self.b_Connect.place(x=280, y=53)

        self.b_Disconnect = Button(self.r, text='연결 해제', command=self.release_server)
        self.b_Disconnect.place(x=355, y=53)

        self.b_Close = Button(self.r, text='닫기', command=exit)
        self.b_Close.place(x=430, y=53)

        self.l_Nickname = Label(self.r, text='닉네임 : ')
        self.l_Nickname.place(x=18, y=84)

        self.e_Nickname = Entry(self.r)
        self.e_Nickname.place(x=82, y=86)

        self.l_Reception = Label(self.r, text='수신')
        self.l_Reception.place(x=20, y=110)

        self.t_Reception_area = ScrolledText(self.r, height=20, width=63)
        self.t_Reception_area.place(x=20, y=135)

        self.l_Send = Label(self.r, text='송신')
        self.l_Send.place(x=20, y=405)

        self.t_Send_area = ScrolledText(self.r, height=8, width=55)
        self.t_Send_area.place(x=20, y=430)

        self.b_Send = Button(self.r, text='전송', command=self.send_switch)
        self.b_Send.place(x=430, y=430, relheight='0.2', relwidth='0.095')

        self.t_Send_area.bind('<Return>', self.enter_press)  # 엔터 키와 바인드

    def connect_server(self):   # 서버 접속 처리 메서드
        self.e_IP['state'] = 'readonly'
        self.e_Port['state'] = 'readonly'
        self.b_Connect['state'] = 'disabled'
        self.b_Disconnect['state'] = 'active'
        self.T_F_Discon = False

        IP = self.e_IP.get()
        PORT = int(self.e_Port.get())

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((IP, PORT))

        Thread(target=self.message_send, args=(self.client_socket, )).start()
        Thread(target=self.message_recv, args=(self.client_socket, )).start()

    def release_server(self):   # 서버 연결 해제 처리 메서드
        self.e_IP['state'] = 'normal'
        self.e_Port['state'] = 'normal'
        self.b_Connect['state'] = 'active'
        self.b_Disconnect['state'] = 'disabled'
        self.T_F_Discon = True

    def send_switch(self):  # 메시지 전송 전 처리 작업 메서드
        self.T_F_send = True

    def message_send(self, client_socket):  # 메시지 전송 메서드
        while True:
            if self.T_F_send:
                nickname = self.e_Nickname.get().strip() + ':'
                if nickname == ':':
                    nickname = 'Unknown:'
                message = self.t_Send_area.get(1.0, "end").strip()
                data = nickname + message
                client_socket.send(data.encode())
                self.t_Send_area.delete(1.0, "end")
                self.T_F_send = False
            else:
                if self.T_F_Discon:
                    client_socket.close()
                    exit()
                sleep(0.1)

    def message_recv(self, client_socket):  # 메시지 수신 메서드
        while True:
            try:
                data = client_socket.recv(1024)
                self.t_Reception_area.insert("end", str(data.decode()) + '\n')
                self.t_Reception_area.yview(END)
                self.t_Reception_area.see('end')
            except ConnectionAbortedError as e:
                self.t_Reception_area.insert("end", '\n[알림] 접속을 종료합니다.\n')
                self.t_Reception_area.yview(END)
                exit()

    def enter_press(self, e):
        self.send_switch()


if __name__ == "__main__":
    TCP_ChatClient()
    mainloop()