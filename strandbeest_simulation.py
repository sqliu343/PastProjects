# This code is inspired by wolfram mathematica 
# code obtained from this website:
# http://community.wolfram.com/groups/-/m/t/863933

# Slider code is based off of code gotten from
# a tutorial python tkinter website:
# https://www.python-course.eu/tkinter_sliders.php

import math as m
from tkinter import Tk, Canvas, Frame, BOTH, ALL, Scale, Button, Pack, COMMAND, HORIZONTAL

class Draw(Frame):
    '''
    Draws a pair of legs for a
    strandbeest. There are sliders
    for each leg length, which
    shows trajectories.
    '''
    
    def __init__(self):
        super().__init__()
        
        self.canvas = Canvas(self)
        
        # Setting up the variables
        self.theta0 = 0
        self.theta1 = 0
        self.array = []
        self.w_i = []
        self.lens = [0] * 12
        self.ar = []
        
        self.master.title("Jansen Linkage")
        self.pack(fill=BOTH, expand = 1)
        
    def sliderLinks(self):
        '''
        Sets up twelve sliders for each of the 
        lengths of the legs.
        '''
        lens = [38, 7.8, 15, 50, 41.5, 61.9, 39.3,
                   55.8, 39.4, 36.7, 49, 65.7]
        # Making sliders
        for i in range(len(lens)):
            self.w_i.append(Scale(self, from_=lens[i]-7, to=lens[i]+7, 
                            orient=HORIZONTAL, resolution=0.1, borderwidth=0,
                            width=5, length=200))
            self.w_i[i].set(lens[i])
            self.w_i[i].pack()

    # Begin parts of code with calculations
    def crossProd(self, x, y):
        '''
        Calculates the cross product of two 3 x 1
        vectors, x and y. Returns this product.
        '''
        return [x[1] * y[2] - x[2] * y[1],
             y[0] * x[2] - y[2] * x[0],
             x[0] * y[1] - x[1] * y[0]]
    
    def returnSignCross(self, x, y):
        '''
        For the cross vector of x and y, return the
        sign of its last element. Returns -1 for a
        negative number, 1 for a positive, and 0
        for 0.
        '''
        n = self.crossProd(x, y)[2]
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0
    
    def circIntersect(self, p1, p2, r1, r2, position):
        ''' 
        Calculate the circle intersection points
        in the format (p1, p2, r1, r2, position) where
        p1 and p2 represent the circle centers [x, y]
        array and r1 and r2 represent their respective
        radii. Position is either 'l' or 'r' (for left
        and right, respectively) dependent on whether
        the points we want to find are to the left or 
        right of the p1 and p2. 
        '''
        d = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
        x = (d**2 - r2**2 + r1**2) / (2 * d)
        y = (r1**2 - x**2)**0.5
        # Calculate unit vectors for the two points
        v1 = [(p2[0] - p1[0]) / d, (p2[1] - p1[1]) / d]
        v2 = [(p1[1] - p2[1]) / d, (p2[0] - p1[0]) / d]
        # Calculate intersections of the two circles
        p = [p1_i + x * v1_i for p1_i, v1_i in zip(p1, v1)]
        sol1 = [p_i + y * v2_i for p_i, v2_i in zip(p, v2)]
        sol2 = [p_i - y * v2_i for p_i, v2_i in zip(p, v2)]
        # Figure out which side of the two points the solution is
        vp = [p2_i - p1_i for p2_i, p1_i in zip(p2, p1)]
        sdist1 = [sol1_i - p1_i for sol1_i, p1_i in zip(sol1, p1)]
        sdist2 = [sol2_i - p1_i for sol2_i, p1_i in zip(sol2, p1)]
        vp.append(0)
        sdist1.append(0)
        sdist2.append(0)
        s1 = self.returnSignCross(vp, sdist1)
        s2 = self.returnSignCross(vp, sdist2)
        # Checks to see if answer should be to the left
        sr = -1
        if position == 'l':
            sr = 1
        # Figures out which solution to return
        if sr == s1:
            return sol1
        if sr == s2:
            return sol2
        
    def findPoints(self, theta, lens):
        '''
        Taking an angle theta (in degrees), the
        function returns the positions of all of
        the linkage end points. lens represents
        a list of length 12 for the linkage lens.
        Note that three points are fixed in the
        entire system.
        '''
        multiplier = 2
        p1 = [0, 0]
        p4 = [lens[0] * multiplier, -lens[1] * multiplier]
        p11 = [-lens[0] * multiplier, -lens[1] * multiplier]
        # Crank of the strandbeest
        p2 = [lens[2] * m.cos(theta) * multiplier, lens[2] * m.sin(theta) * multiplier]
        # Left leg coordinates
        p3 = self.circIntersect(p2, p4, lens[3] * multiplier, lens[4] * multiplier, 'l')
        p6 = self.circIntersect(p2, p4, lens[5] * multiplier, lens[6] * multiplier, 'r')
        p5 = self.circIntersect(p3, p4, lens[7] * multiplier, lens[4] * multiplier, 'l')
        p8 = self.circIntersect(p5, p6, lens[8] * multiplier, lens[9] * multiplier, 'l')
        p7 = self.circIntersect(p6, p8, lens[10] * multiplier, lens[11] * multiplier, 'r')
        # Right leg coordinates
        p10 = self.circIntersect(p2, p11, lens[3] * multiplier, lens[4] * multiplier, 'r')
        p13 = self.circIntersect(p2, p11, lens[5] * multiplier, lens[6] * multiplier, 'l')
        p12 = self.circIntersect(p10, p11, lens[7] * multiplier, lens[4] * multiplier, 'r')
        p14 = self.circIntersect(p12, p13, lens[8] * multiplier, lens[9] * multiplier, 'r')
        p15 = self.circIntersect(p13, p14, lens[10] * multiplier, lens[11] * multiplier, 'l')
        return [p1, p2, p3, p4, p5, p6, p7, p8,
                p10, p11, p12, p13, p14, p15]

    def coordTransform(self, plist):
        '''
        Takes plist, a list of size 14. It
        contains 14 points (list size 2). It
        transforms these coordinates such that
        they can be shown in tkinter.
        '''
        offset = 225
        for i in range(14):
            plist[i][0] = plist[i][0] * 1 + offset
            plist[i][1] = plist[i][1] * -1 + offset * 1/3
            i += 1
        return plist

    def drawLinks(self, theta, lens):
        '''
        Taking an angle theta (in degrees), the
        function returns the line segments that
        represent the strandbeest linkages.
        lens represents the list of size 12 for
        linkage lengths.
        '''
        # Finds the coordinate of the line segment points
        plist  = self.coordTransform(self.findPoints(theta, lens))
        array = []
        # Append all of the line creations to an array
        array.append(self.canvas.create_line(plist[0][0], plist[0][1], plist[1][0], plist[1][1]))
        array.append(self.canvas.create_line(plist[1][0], plist[1][1], plist[2][0], plist[2][1]))
        array.append(self.canvas.create_line(plist[2][0], plist[2][1], plist[3][0], plist[3][1]))
        array.append(self.canvas.create_line(plist[0][0], plist[0][1], plist[3][0], plist[3][1]))
        array.append(self.canvas.create_line(plist[1][0], plist[1][1], plist[5][0], plist[5][1]))
        array.append(self.canvas.create_line(plist[3][0], plist[3][1], plist[5][0], plist[5][1]))
        array.append(self.canvas.create_line(plist[2][0], plist[2][1], plist[4][0], plist[4][1]))
        array.append(self.canvas.create_line(plist[3][0], plist[3][1], plist[4][0], plist[4][1]))
        array.append(self.canvas.create_line(plist[4][0], plist[4][1], plist[7][0], plist[7][1]))
        array.append(self.canvas.create_line(plist[5][0], plist[5][1], plist[7][0], plist[7][1]))
        array.append(self.canvas.create_line(plist[5][0], plist[5][1], plist[6][0], plist[6][1]))
        array.append(self.canvas.create_line(plist[6][0], plist[6][1], plist[7][0], plist[7][1]))
        array.append(self.canvas.create_line(plist[0][0], plist[0][1], plist[9][0], plist[9][1]))
        array.append(self.canvas.create_line(plist[8][0], plist[8][1], plist[9][0], plist[9][1]))
        array.append(self.canvas.create_line(plist[1][0], plist[1][1], plist[8][0], plist[8][1]))
        array.append(self.canvas.create_line(plist[1][0], plist[1][1], plist[11][0], plist[11][1]))
        array.append(self.canvas.create_line(plist[9][0], plist[9][1], plist[11][0], plist[11][1]))
        array.append(self.canvas.create_line(plist[8][0], plist[8][1], plist[10][0], plist[10][1]))
        array.append(self.canvas.create_line(plist[9][0], plist[9][1], plist[10][0], plist[10][1]))
        array.append(self.canvas.create_line(plist[10][0], plist[10][1], plist[12][0], plist[12][1]))
        array.append(self.canvas.create_line(plist[11][0], plist[11][1], plist[12][0], plist[12][1]))
        array.append(self.canvas.create_line(plist[11][0], plist[11][1], plist[13][0], plist[13][1]))
        array.append(self.canvas.create_line(plist[12][0], plist[12][1], plist[13][0], plist[13][1]))
        
        self.canvas.pack(fill=BOTH, expand=1)
        return array

    def moveLinks(self):
        '''
        Takes one angle (in radians) and
        moves the links from that angle
        to the next one in increments of
        pi / 200.
        '''
        lens = self.lens[:]
        # Read all of the slider values
        for i in range(12):
            self.lens[i] = self.w_i[i].get()
        # If slider values are different, plot new trajectory!
        if lens != self.lens:
            for i in self.ar:
                # Clear old trajectory!
                self.canvas.delete(i)
            self.ar = self.drawTrajectories(self.lens)
        nsteps = 200
        for i in self.array:
            # Clear old line segments!
            self.canvas.delete(i)
        self.array = self.drawLinks(self.theta0, self.lens)
        self.theta0 += m.pi / nsteps
        self.canvas.after(10, self.moveLinks)
        
    def drawTrajectories(self, lens):
        '''
        Draws the trajectories of the entire
        linkage system. Ignores stationary
        points. Also draws the movement of 
        the linkage system.
        lens represents the list of size 12
        corresponding to the linkage lens
        '''
        nsteps = 200
        plist = []
        ar = []
        for _ in range(nsteps + 1):
            # Find the whole sequence of points in a full crank revolution
            plist.append(self.coordTransform(self.findPoints(self.theta1, lens)))
            self.theta1 += 2 * m.pi / nsteps
        for n in range(len(plist) - 1):
            for k in range(14):
                # Append the new coordinates that need to be drawn
                ar.append(self.canvas.create_line(plist[n][k][0], plist[n][k][1], 
                                        plist[n + 1][k][0], plist[n + 1][k][1],
                                        fill="#2f7"))
        return ar
        
def main():
    root = Tk()
    root.geometry("450x700+250+0")
    d = Draw()

    # Sliders!
    d.sliderLinks()
    
    # Move the linkages forever!    
    d.moveLinks()
    
    root.mainloop()
    
if __name__ == '__main__':
    main()