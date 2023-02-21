# function to make outline of nut (useful for 3D printing)

import rhinoscriptsyntax as rs
import math

def nut_outline():
    # user input for size (metric)
    items = ["M2", "M3", "M4", "M5", "M6", "M8", "M10"]
    nut_size = rs.MultiListBox(items, "Select nut size", "Nut size")[0]
    nut_size_index = items.index(nut_size)
    
    # draw outline
    ## size list
    size_list = [4, 5.5, 7, 8, 10, 13, 17] 
    width = size_list[nut_size_index]
    
    # some trig
    x_30 = math.tan(math.radians(30)) * (width / 2)
    
    # points
    p1 = [(width * -0.5), x_30, 0]
    p2 = [0, 2* x_30, 0]
    p3 = [(width * 0.5), x_30, 0]
    p4 = [(width * 0.5), x_30 * -1, 0]
    p5 = [0, -2 * x_30, 0]
    p6 = [(width * -0.5), x_30 * -1, 0]
    
    # crv
    crv = rs.AddPolyline([p1, p2, p3, p4, p5, p6, p1]) 
    
    # return
    return crv

nut_outline()
