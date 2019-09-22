#!/usr/bin/env python

import matplotlib
matplotlib.use('TKAgg')
import socket
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import pickle
import sqlite3



# setup database
db = sqlite3.connect('raw_data.db')
cursor = db.cursor()

cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE \
type='table' AND name='raw_data' ''')

#if table exists, delete and recreate
if cursor.fetchone()[0]==1 :
	print('Table exists, delete first')
	cursor.execute('''
	DROP TABLE raw_data
	''')
	db.commit()

cursor.execute('''
   CREATE TABLE raw_data(time double PRIMARY KEY, gain FLOAT)
''')
db.commit()

# setup socket
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
socket_conn, addr = s.accept()

# functions
# todo: move functions to module
def recieve_data():
	while True:
		 data = socket_conn.recv(1024)
		 if not data:
			 break
		 socket_conn.sendall(data)
		 msg = pickle.loads(data)
		 time = float(msg[0])
		 gain = float(msg[1])
		 yield time , gain
	socket_conn.close()

def passer():
    for line in recieve_data():
		yield line

class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.gdata = [0]
        self.line = Line2D(self.tdata, self.gdata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self,passer):
        t , g = passer
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.gdata = [self.gdata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()
        self.tdata.append(t)
        self.gdata.append(g)

        cursor.execute('''INSERT INTO raw_data(time, gain)
        VALUES(?,?)''',(float(t),float(g)))
        print(t,g)
        db.commit()

        self.line.set_data(self.tdata, self.gdata)
        return self.line,


# main
fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, passer, interval=10,
                              blit=False)
plt.title("recieved data")
plt.show()

db.close()
