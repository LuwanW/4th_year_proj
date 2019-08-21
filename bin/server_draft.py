#!/usr/bin/env python

import socket
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib import style
import pickle
# Create figure for plotting

time_list = []
gain_list = []

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()


fig, ax1 = plt.subplots()
ax1.set_ylim(-.1, 1.1)
ax1.set_xlim(0, 2)

def recieve_data():
	while True:
		 data = conn.recv(1024)
		 if not data:
			 break
		 conn.sendall(data)
		 msg = pickle.loads(data)
		 time = float(msg[0])
		 gain = float(msg[1])
		 yield time , gain
	conn.close()



def animate(i):
    xs = []
    ys = []
    for line in recieve_data():
        if len(xs) < 50:
            x, y = line
            #print(x,y)
            xs.append(float(x))
            ys.append(float(y))
        else:break
    print(xs,ys)
    ax1.clear()
    ax1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()





