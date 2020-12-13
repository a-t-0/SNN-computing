import tkinter as tk
import networkx as nx


class NetworkGUI:
    def __init__(self):
        self.canvas_width = 800
        self.canvas_height = 500


def draw_graph(canvas, graph):
    '''
    Inputs:
        graph       -       a networkx Graph object
        canvas      -       the canvas to draw on
    TODO:
        currently, the graph area is hardcoded to be square and 50 pixels smaller than the canvas to make sure all nodes
        are drawn completely, fix ugly hardcoded positioning and maybe make dynamic?
    '''
    layout = nx.spring_layout(graph, scale=min(CANVAS_WIDTH-50, CANVAS_HEIGHT-50)/2)
    # networkx places nodes in a box centered at zero, if scale is specified as x, then nodes will be in
    # [-x, x]
    # for now, place all nodes in a square with size dependent on the smaller of the canvas dimensions
    width = min(CANVAS_WIDTH-50, CANVAS_HEIGHT-50)/2

    #  Nodes

    for node in layout.keys():
        pos = layout[node]
        # shift positions to right upper quadrant instead of centered around 0
        x,y = pos[0], pos[1]
        x,y = translate_pos(x,y)
        place_node(canvas, x,y)

    #  Connections

    for edge in graph.edges():
        n1, n2 = edge
        n1pos = layout[n1]
        n2pos = layout[n2]
        x1,y1 = translate_pos(n1pos[0], n1pos[1])
        x2,y2 = translate_pos(n2pos[0], n2pos[1])
        draw_connection(canvas, (x1,y1), (x2,y2))



def place_node(canvas, xpos, ypos, diam=20):
    x1 = xpos - diam/2
    y1 = ypos - diam/2
    x2 = xpos + diam/2
    y2 = ypos + diam/2

    canvas.create_oval(x1,y1,x2,y2,outline="black", fill="black")
    print(f"node drawn at: {xpos, ypos}")


def draw_connection(canvas, n1pos, n2pos):
    canvas.create_line(n1pos[0], n1pos[1], n2pos[0], n2pos[1])

def translate_pos(x,y, padding=50):
    '''
    translate position generated by networkx to canvas position
    '''
    width = min(CANVAS_WIDTH-padding, CANVAS_HEIGHT-padding)/2
    x_canv = x/2 + width/2 + padding/2
    y_canv = y/2 + width/2 + padding/2
    return x_canv, y_canv



### TEST SETUP ###

G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,1)


### GUI LOOP ###

top = tk.Tk()
top.title("test gui")
canv = tk.Canvas(top, width=800, height=500, bg='white')
draw_graph(canv, G)
canv.pack()
top.mainloop()