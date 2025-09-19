# The following code was written by MIT
# graduate student, Sandra Q. Liu, for
# her 18.0851 final project. If you 
# have any questions about the project,
# feel free to contact her by email:
# sqliu@mit.edu

# Note: A bunch of print statements are
# scattered around from debugging.

import numpy as np
from tkinter import Tk, ttk, Canvas, Frame, Radiobutton, Label, BOTH, IntVar, Button

class trussAnalysis(Frame):
    def __init__(self):
        super().__init__()
        
        self.canvas = Canvas(self)
        
        # For reading radio button presses
        self.v = IntVar()
        
        self.master.title("Truss Analysis")
        self.pack(fill=BOTH, expand = 1)
        
        # Initializing variables to store them for analysis
        self.nodes = []
        self.singlink = [] # Temporary storage for links before it gets compiled into self.links
        self.links = []
        self.supports = []
        self.trussmat = []
    
    def initMatrix(self, nodes, links, supports):
        '''
        Takes a list of lists of size 2,
        which represents each of the 
        coordinates [x, y] of the nodes
        in the truss, the incidence
        matrix based off the numbering
        of the nodes, and a list of the
        node numbers that are supports.
        Updates the size of the truss 
        matrix.
        '''
        for i in range(len(links)):
            self.trussmat.append([])
            for j in range(len(links[0]) - len(supports)):
                self.trussmat[i].append(0)
                self.trussmat[i].append(0)
                    
    def calcVec(self, node1, node2):
        '''
        Takes two nodes (lists of size 2)
        and returns the angle of the line
        relative to the 'horizontal' and
        the length of the line in the form
        of [length, angle].
        '''
        ydiff = node2[1] - node1[1]
        xdiff = node2[0] - node1[0]
        length = (ydiff**2 + xdiff**2)**0.5
        angle = np.arctan2(ydiff, xdiff)
        return [length, angle]
    
    def trussMatrix(self, nodes, links, supports):
        '''
        Takes a list of lists of size 2,
        which represents each of the 
        coordinates [x, y] of the nodes
        in the truss, the incidence
        matrix based off the numbering
        of the nodes (note that the 
        numbering is based off of order
        of the nodes in the list of
        coordinates), and a list of the
        node numbers that are supports. 
        Updates the truss matrix.
        '''
        self.initMatrix(nodes, links, supports)
        for i in range(len(links)):
            # Index to update the truss matrix.
            index = 0
            for j in range(len(nodes)):
                if links[i][j] == -1:
                    node1 = nodes[j]
                if links[i][j] == 1:
                    node2 = nodes[j]            
            for j in range(len(nodes)):
                x = 0
                y = 0
                if abs(links[i][j]) == 1:
                    multiplier = links[i][j] * -1
                    [length, theta] = self.calcVec(node1, node2)
                    #print(length, theta)
                    
                    # We round to the nearest 50 to limit the error when lines aren't
                    # perfectly horizontal or vertical. We also multiply by length so
                    # that we can pretend the nodes are fairly vertical/horizaontal 
                    # of one another and determine stability more accurately.
                    x = int(length * np.cos(theta) * multiplier / 50) * 50
                    y = int(length * np.sin(theta) * multiplier / 50) * 50
                # Parameter to check if the node is a support or not
                # If it is, we neglect to add it to our truss matrix
                add = True
                for fixed in supports:
                    if j == fixed:
                        add = False
                if add:
                    #print("Adding!", x, y)
                    self.trussmat[i][index * 2] = x
                    self.trussmat[i][index * 2 + 1] = y
                    index += 1
    
    def linIndep(self, matrix):
        '''
        Takes the incidence matrix of a truss
        and returns 'True' if the matrix has
        linearly indepedent rows and 'False'
        if it does not. 
        
        Incidence matrix is a list of lists.
        '''
        marray = np.array(matrix)
        if len(matrix) < len(matrix[0]):
            return False
        if len(matrix) > len(matrix[0]):
            #print("Actually, this is overconstrained!")
            return True
        print(np.linalg.det(marray))
        return not np.linalg.det(marray) == 0
    
    def trussStable(self, nodes, links, supports):
        '''
        Takes a list of lists of size 2,
        which represents each of the 
        coordinates [x, y] of the nodes
        in the truss, the incidence
        matrix based off the numbering
        of the nodes (note that the 
        numbering is based off of order
        of the nodes in the list of
        coordinates), and a list of the
        node numbers that are supports
        Returns True if the truss is 
        stable. Else, it returns False.
        Supports starts at index = 0.
        
        If matrix is overconstrained, it
        will return 'True.'
        '''
        self.trussMatrix(nodes, links, supports)
        return self.linIndep(self.trussmat)
    
    def incMatrix(self, singlink):
        '''
        Takes an even list of node
        values, where every two nodes
        represents the end points of a
        link. Updates the incidence
        matrix (of the form of a list
        of lists).
        '''
        # Clear these variables out so we can continually update our truss without restarting.
        self.links = []
        self.trussmat = []
        for i in range(int(len(singlink) / 2)):
            self.links.append([])
            for j in range(len(self.nodes)):
                self.links[i].append(0)
        for i in range(0, len(singlink), 2):
            if singlink[i] < singlink[i + 1]:
                node1 = singlink[i]
                node2 = singlink[i + 1]
            else:
                node1 = singlink[i + 1]
                node2 = singlink[i]
            self.links[int(i / 2)][node1] = -1
            self.links[int(i / 2)][node2] = 1
    
    def calcTruss(self):
        '''
        Similar to trussStable, except
        it takes its inputs from the 
        stored values obtained from user
        input in GUI.
        '''
        self.incMatrix(self.singlink)
        a = self.trussStable(self.nodes, self.links, self.supports)
        #print(self.trussmat)
        self.ans.configure(text=str(a))
    
    def test(self):
        '''
        These be tests - if you do not
        have the GUI and just want to 
        test the math.
        '''
        nodes = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 2], [1, 2]]
        links = [[-1, 1, 0, 0, 0, 0], [0, -1, 0, 0, 1, 0], [0, 0, 0, 0, -1, 1], [0, 0, -1, 0, 0, 1], [0, 0, -1, 0, 1, 0], [0, -1, 0, 1, 0, 0], [0, 0, -1, 1, 0, 0]]
        #links = links + [[-1, 0, 1, 0, 0, 0]]
        
        #nodes = [[0, 0], [0, 1], [1, 1], [1,0]]
        #links = [[-1, 1, 0, 0], [0, -1, 1, 0], [0, -1, 0, 1], [0, 0, -1, 1]]
        
        supports = [0, 3]
        a = self.trussStable(nodes, links, supports)
        
        print("Matrix is stable?")
        
        print(a)
    
    #################
    # The following functions are all functions
    # that use tkinter.
    
    def createGUI(self, root):
        '''
        Creates a GUI using tkinter so
        that a user can draw a truss.
        '''
        self.lbl = Label(root, text="Welcome to the truss building GUI! Select 'Node' to get started!")
        
        self.lbl.pack()
        
        self.r1 = Radiobutton(root, text='Node', variable=self.v, value=1, command=self.clicked)
        self.r2 = Radiobutton(root, text='Link', variable=self.v, value=2, command=self.clicked)       
        self.r3 = Radiobutton(root, text='Support', variable=self.v, value=3, command=self.clicked)
        
        self.r1.pack()
        self.r2.pack()
        self.r3.pack()
        
        self.button = Button(root, text='Calculate! Truss stable?', command=self.calcTruss)
        
        self.button.pack()
        
        self.ans = Label(root, text=' ')
        
        self.ans.pack()
        
    def clicked(self):
        '''
        Depending on the clicked button
        a different functionality will
        be performed (drawing nodes,
        links, supports).
        '''
        if self.v.get() == 1:
            self.lbl.configure(text="'Node' selected. Click anywhere to create a node of the truss. Try to keep nodes vertical/horizontal of one another!")
            self.canvas.bind("<Button-1>", self.drawNode)
            
        if self.v.get() == 2:
            self.lbl.configure(text="'Link' selected. Click on two nodes to connect them together.")
            self.canvas.bind("<Button-1>", self.drawLink1)
            
        if self.v.get() == 3:
            self.lbl.configure(text="'Support' selected. Click on any node to make it into a support.")
            self.canvas.bind("<Button-1>", self.drawSupport)
            
        self.canvas.pack(fill=BOTH, expand=1)
            
    def drawNode(self, event):
        '''
        Draws a node once a mouse click
        is detected. Stores the nodes
        in self.nodes.
        '''
        x, y = event.x, event.y
        x1, y1 = (x - 4), (y - 4)
        x2, y2 = (x + 4), (y + 4)
        self.canvas.create_oval(x1, y1, x2, y2, fill = "black")
        self.nodes.append([x, y])
        #print(self.nodes)
    
    # The following two functions call on each other
    # to let you draw a line between two clicked points.
    def drawLink1(self, event):
        '''
        Stores the first node so that
        it can create a line once it
        calls upon the second mouse
        click event.
        '''
        self.x1, self.y1 = event.x, event.y
        # Check for proximity of click to existing node
        for i in range(len(self.nodes)):
            x = self.nodes[i][0]
            y = self.nodes[i][1]
            if abs(self.x1 - x) <= 8 and abs(self.y1 - y) <= 8:
                self.lbl.configure(text="First node selected!")                
                self.x1 = x
                self.y1 = y
                self.canvas.bind("<Button-1>", self.drawLink2)
                self.singlink.append(i)
    
    def drawLink2(self, event):
        '''
        Stores the second node so
        that we can draw the full
        link. Stores the number of
        the nodes connecting the
        line. Afterwards, it
        returns to asking for the
        first node.
        '''
        self.x2, self.y2 = event.x, event.y
        # Check for proximity of click to existing node
        for i in range(len(self.nodes)):
            x = self.nodes[i][0]
            y = self.nodes[i][1]
            if abs(self.x2 - x) <= 8 and abs(self.y2 - y) <= 8:
                self.lbl.configure(text="Link created! Click on two more nodes to connect them together.")                
                self.x2 = x
                self.y2 = y
                self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="black")
                self.canvas.bind("<Button-1>", self.drawLink1)
                # We store in self.singlink temporarily so that user can add more nodes if needed
                self.singlink.append(i)
                #print(self.singlink)
        
    def drawSupport(self, event):
        '''
        Draws a support on the
        selected node. Stores
        in self.supports.
        '''
        x, y = event.x, event.y
        # Check for proximity of click to existing node        
        for i in range(len(self.nodes)):
            xnode = self.nodes[i][0]
            ynode = self.nodes[i][1]
            if abs(x - xnode) <= 8 and abs(y - ynode) <= 8:
                self.lbl.configure(text="Support created! Click on more nodes to create more supports.")
                x1, y1 = xnode - 10, ynode + 8
                x2, y2 = xnode + 10, ynode + 8
                x3, y3 = xnode, ynode - 9
                self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="black")
                self.supports.append(i)
                #print(self.supports)
        
def main():
    # Comment out the two lines below if you want to run the test.
    root = Tk()
    root.geometry("700x700")
    
    truss = trussAnalysis()
    
    # Uncomment line 351 if you want to run the math test and not use the interface.
    # You will also have to comment out truss.createGUI(root) and root = Tk() and
    # root.geometry("700x700")
    #truss.test()
    
    # Comment out line below if you want to run the truss.test() function above.
    truss.createGUI(root)

    root.mainloop()
    
if __name__ == '__main__':
    main()