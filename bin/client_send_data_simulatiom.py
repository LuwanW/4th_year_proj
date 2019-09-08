#!/usr/bin/env python
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        #self object, ax graph, maxt max time frame, dt 0.02 capture frequency, this import data into function
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        # set amplitude limits
        self.ax.set_ylim(-.1, 1.1)
        # set x axis limits 
        self.ax.set_xlim(0, self.maxt)
        
    # updates data
    def update(self, y):
        #starts from last data (-1)
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            # self.tdata[-1] is last value, the resultant array is size 1 with value lastT
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            #set frame to current point + maxt
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        #get t for next point
        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)

        # dump data and send data through socket
        # todo: use real measured data instead of simulation
        print(t,y)
        
        msg = [t,y]
        data=pickle.dumps(msg)
        s.send(data)
        return self.line,

# to use remove random generator
def emitter(p=0.03):
    'return a random value with probability p, else 0'
    while True:
        v = np.random.rand(1)
        if v > p:
            yield 0.
        else:
            yield np.random.rand(1)

# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,
                              blit=True)

plt.title("sent data")
plt.show()
