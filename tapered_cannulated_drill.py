"""
Python script tapered_cannulated_drill.py
Scott Telfer 2022-12-28
email: scott.telfer@gmail.com
"""

import rhinoscriptsyntax as rs

def tapered_cannulated_drill(prox_rad, dist_rad, can_rad, drill_len):
    """
    Create solid model of tapered drill bit with canulated center
    
    :param float prox_rad: radius of proximal end of drill
    :param float dist_rad: radius of distal end of drill
    :param float can_rad: radius of cannulated hole
    :param float drill_len: length of drill bit
    :return: solid model of drill
    """
    
    # check inputs
    if prox_rad < dist_rad:
        raise ValueError("prox_rad must be larger than dist_rad")
    if dist_rad < can_rad:
        raise ValueError("dist_rad must be larger than can_rad")
    
    # chuck grip
    chuck_line = rs.AddPolyline([[0, -20, 0], [0, -20, 2.8], [0, -19.8, 3], 
                                 [0, -0.2, 3], [0, 0, 3.2]])
    axis = rs.AddLine([0, 0, 0], [0, 1, 0])
    chuck_grip = rs.AddRevSrf(chuck_line, axis)
    rs.DeleteObject(chuck_line)
    
    # drill cone
    cone_line = rs.AddPolyline([[0, 0, 0], [0, 0, prox_rad], 
                                [0, drill_len, dist_rad], [0, drill_len, 0]])
    
    cone = rs.AddRevSrf(cone_line, axis)
    drill_bit = rs.BooleanUnion([chuck_grip, cone])
    rs.DeleteObject(cone_line)
    
    # chamfer end
    chamfer_line = rs.AddPolyline([[0, drill_len, 0], 
                                   [0, drill_len, dist_rad], 
                                   [0, drill_len + dist_rad, 0]])
    chamfer_end = rs.AddRevSrf(chamfer_line, axis)
    drill_bit = rs.BooleanUnion([drill_bit, chamfer_end])
    rs.DeleteObjects([chamfer_line, axis])
    
    # flutes
    cut1_crv = rs.AddPolyline([[3.2, -0.1, -20], [3.2, -0.1, 2.5], 
                               [20, -0.1, 2.5], [20, -0.1, -20], 
                               [3.2, -0.1, -20]])
    cut1 = rs.AddPlanarSrf(cut1_crv)
    loft_line1 = rs.AddLine([3, -0.1, 2.5], 
                            [can_rad + 0.25, drill_len + dist_rad + 0.2, 0.05])
    flute1 = rs.ExtrudeSurface(cut1, loft_line1)
    flute2 = rs.CopyObject(flute1)
    flute2 = rs.RotateObject(flute2, [0, 0, 0], 180, [0, 1 ,0])
    drill_bit = rs.BooleanDifference(drill_bit, [flute1, flute2])
    rs.DeleteObjects([cut1_crv, cut1, loft_line1])
    
    # cannulation
    canu = rs.AddCylinder(rs.WorldZXPlane(), drill_len + 50, can_rad)
    canu = rs.MoveObject(canu, [0, -25, 0])
    drill_bit = rs.BooleanDifference(drill_bit, canu)
    
    # return finished model
    return drill_bit

tapered_cannulated_drill(5, 2, 1, 25)