# from threading import Thread
# import numpy as np
# import math

from ROB.HexaplotReceiver import HexaplotReceiver

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
import mpl_toolkits.mplot3d.art3d as art3d


class Hexaplot:

    def __init__(self,hex_coord, ax_limits=None, plt_pause_value=0.05, dot_color='white', line_color='black', show_lines=False):
        self.hex_coord = hex_coord
        self.height = 0.151

        if ax_limits is None:
            ax_limits = [10, 10, 2]
        self.hr = HexaplotReceiver()
        self.ax_limits = ax_limits
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        #self.ax2 = self.fig.add_subplot(122)


        # Setting the axes properties
        self.ax.set_xlim3d([-self.ax_limits[0], self.ax_limits[0]])
        #self.ax.set_xlabel('X')
        self.ax.set_ylim3d([-self.ax_limits[1], self.ax_limits[1]])
        #self.ax.set_ylabel('Y')
        self.ax.set_zlim3d([-self.ax_limits[2], self.ax_limits[2]])
        #self.ax.set_zlabel('Z')
        self.ax.grid(False)



        # Setting the axes properties
        #self.ax2.set_xlim([-1.7, 1.7])
        #self.ax2.set_xlabel('X')
        #self.ax2.set_ylim([0, 1.2])
        #self.ax2.set_ylabel('Y')


        # Get rid of the ticks
        self.ax.axes.get_xaxis().set_ticks([])
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_zaxis().set_ticks([])

        # Get rid of the panes
        self.ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        # Get rid of the spines
        self.ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        #self.ax2.spines['top'].set_visible(False)
        #self.ax2.spines['right'].set_visible(False)

        self.center_x_offset = 0
        self.center_y_offset = 0
        self.center_z_offset = 0

        self.ax.set_title('Hexapod Simulation')
        self.plt_pause_value = plt_pause_value
        self.show_lines = show_lines

        self.dot_color = dot_color
        self.line_color = line_color

        self.last_scatter_list = []
        self.last_scatter_list2 = []
        self.last_line_list = []
        self.current_points = []
        self.current_lines = []
        self.first = True


    def update_points(self, points=None, tPoints=None): # VL, ML, HL, VR, MR, HR

        if tPoints is None:
            tPoints = [0, 0]

        if points:
            if self.last_scatter_list:
                for ls in self.last_scatter_list:
                    ls.remove()
                self.last_scatter_list = []

            if self.show_lines:
                self.plot_lines(points)
            if len(self.last_scatter_list2) == 1:
                self.last_scatter_list2[0].remove()
                self.last_scatter_list2 = []
            last_scatter =self.ax2.scatter(tPoints[0],tPoints[1], c="Red", linewidths=2)
            self.last_scatter_list2.append(last_scatter)

            for p in points:
                x1 = p[0]+self.center_x_offset
                y1 = p[1]+self.center_y_offset
                z1 = p[2]+self.center_z_offset
                last_scatter = self.ax.scatter(x1, y1, z1, c=self.dot_color)
                self.last_scatter_list.append(last_scatter)

    def show_plot(self):
        while True:
            data = self.hr.getData()
            if data != None:
                formatted_data = []
                for line in data:
                    formatted_data.append([[line[0][0] * 100, line[0][1] * 100, line[0][2] * 100], [line[1][0] * 100, line[1][1] * 100,
                                                                                   line[1][2] * 100]])
                data = formatted_data
                print(data)
                self.plot_lines(data)
            #self.update_points(data[0], data[2])
            plt.pause(self.plt_pause_value)



    def plot_lines(self, lines):   #[[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]
        if lines != None:
            self.ax.lines.clear()
            if self.last_scatter_list:
                for ls in self.last_scatter_list:
                    ls.remove()
                self.last_scatter_list = []
            for line in lines:
                x = [line[0][0], line[1][0]]
                y = [line[0][1], line[1][1]]
                z = [line[0][2], line[1][2]]
                self.last_line_list.append(self.ax.plot(x, y, z, c=self.line_color))
                self.last_scatter_list.append(self.ax.scatter(x[0], y[0], z[0], c=self.dot_color))
                self.last_scatter_list.append(self.ax.scatter(x[1], y[1], z[1], c=self.dot_color))


def plotStart():
    hex_coord = [[0.160,0.087],[0.160, -0.087],[0, 0.1615],[-0.160,-0.087],[-0.160, 0.087],[0, -0.1615]]
    for coord in hex_coord:
        coord[0] *= 100
        coord[1] *= 100
    print(hex_coord)
    hp = Hexaplot(hex_coord, ax_limits=[20,20,15], dot_color='green', line_color='black', show_lines=True)

    # [[3,1.5],[1,5],[3,8.5],[7,1.5],[9,5],[7,8.5]]

    # Draw a circle on the x=0 'wall'
    l1 = Circle(hex_coord[0],  7, alpha=0.5)
    l2 = Circle(hex_coord[1],  7, alpha=0.5)
    l3 = Circle(hex_coord[2],  7, alpha=0.5)
    l4 = Circle(hex_coord[3],  7, alpha=0.5)
    l5 = Circle(hex_coord[4],  7, alpha=0.5)
    l6 = Circle(hex_coord[5],  7, alpha=0.5)

    circlesB = [l6, l3, l4, l5]
    circlesF = [l1, l2]

    for circle in circlesF:
        circle.set_color("red")
        hp.ax.add_patch(circle)
        art3d.pathpatch_2d_to_3d(circle, z=0, zdir="z")


    for circle in circlesB:
        circle.set_color("green")
        hp.ax.add_patch(circle)
        art3d.pathpatch_2d_to_3d(circle, z=0, zdir="z")


    groupA = Polygon((hex_coord[0], hex_coord[5], hex_coord[4]), alpha=0.4)
    groupB = Polygon((hex_coord[1], hex_coord[3], hex_coord[2]), alpha=0.4)

    groups = [groupA, groupB]

    groupA.set_color("blue")
    groupB.set_color("yellow")
    for group in groups:
        hp.ax.add_patch(group)
        art3d.pathpatch_2d_to_3d(group, z=1, zdir="z")

    hp.show_plot()

if __name__ == "__main__":
    plotStart()