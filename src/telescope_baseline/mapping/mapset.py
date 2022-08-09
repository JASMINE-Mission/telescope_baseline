"""mapping set

 * Lshape -> large_frame  

"""
import numpy as np
import tqdm
from telescope_baseline.mapping.aperture import lb_detector_unit, four_square_convexes, inout_four_square_convexes, ang_detector_unit, lb2ang, ang2lb

def ditheringmap(l_center,b_center,PA_deg,  dithering_width_mm, Ndither, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """make convexes set of (extended) L shape formation
    
    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        dithering_width_mm: dithering width in mm
        Ndither: [Nx,Ny] of the ditherings
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        convexesset: convexes set

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    width=width_mm/EFL_mm
    each_width=each_width_mm/EFL_mm
    dithering_width=dithering_width_mm/width_mm/2
    
    convexesset=[]
    for i in tqdm.tqdm(range(0,Ndither[0])):
        for j in range(0,Ndither[1]):
            pos=ang_detector_unit("R",dithering_width*i,center,PA,width)
            convexes=four_square_convexes(ang_detector_unit("B",dithering_width*j,pos,PA,width), PA, width, each_width)
            convexesset.append(convexes)

    return convexesset


def inout_convexesset(targets,convexesset):
    """checking if targets are in or out (extended) convexesset
    
    Args:
        targats: targets coordinate list (in radian)
        convexesset: convexesset

    Returns:
        answer: inout mask sequence (in = 1 or out = 0 mask), (4, N)
                                             
    """
    
    ans=[]
    for convexes in tqdm.tqdm(convexesset):
        a=inout_four_square_convexes(targets, convexes)
        ans.append(a)

    return ans


def Lshape(l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """make convexes set of (extended) L shape formation
    
    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        convexesset: convexes set

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    width=width_mm/EFL_mm
    each_width=each_width_mm/EFL_mm
    
    convexesset=[]
    convexes=four_square_convexes(center, PA, width, each_width)
    convexesset.append(convexes)
    
    convexes=four_square_convexes(ang_detector_unit("R",0.5,center,PA,width), PA, width, each_width)
    convexesset.append(convexes)
    
    pos=ang_detector_unit("L",left,center,PA,width)
    convexes=four_square_convexes(ang_detector_unit("T",1.0+top,pos,PA,width), PA, width, each_width)
    convexesset.append(convexes)

    convexes=four_square_convexes(ang_detector_unit("T",1.5+top,pos,PA,width), PA, width, each_width)
    convexesset.append(convexes)

    return convexesset

def inout_Lshape(targets,convexesset):
    """checking if targets are in or out (extended) L shape formation
    
    Args:
        targats: targets coordinate list (in radian)
        convexesset: convexesset

    Returns:
        answer: inout mask sequence (in = 1 or out = 0 mask), (4, N)
                                             
    """
    return inout_convexesset(targets,convexesset)

def large_frame(l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """compute large_convex

    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        in/out large frame
    """
    #shift
    l_center,b_center=lb_detector_unit("L",left,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("T",top,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    
    #right L        
    large_convex=[]
    convexesset=Lshape(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=1.0,top=-0.75)
    large_convex.append(convexesset)
    #mid L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    l_center,b_center=lb_detector_unit("B",0.75,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    convexesset=Lshape(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.5)
    large_convex.append(convexesset)

    #left L
    l_center,b_center=lb_detector_unit("L",1.5,l_center,b_center, PA_deg, width_mm=width_mm, EFL_mm=EFL_mm)
    convexesset=Lshape(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
    large_convex.append(convexesset)

    return large_convex


def inout_large_frame(targets,large_convex):
    """in or out large frame

    Args:
        targats: targets coordinate list (in radian)
        large_convex: large_convex
    Returns:
        inout mask sequence of inout mask of four detectors (in = 1 or out = 0 mask), (3,4,N)
    """
    ans=[]
    for convexesset in large_convex:
        a=inout_Lshape(targets,convexesset)
        ans.append(a)

    return ans

def fillgap_large_frame(l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0, left=0.0, top=0.0):
    """fill gap dithering 

    Args:
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
        left: shift to left of the upper two fields 
        top: shift to top of the upper two fields 

    Returns:
        fillgap large convex, (4,3,4,N)
    """
    pos=[]
    pos1=large_frame(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125+left,top=-0.125/2.0+top)
    pos.append(pos1)
    pos2=large_frame(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125+left,top=-0.125/2.0+top)
    pos.append(pos2)
    pos3=large_frame(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=0.125+left,top=0.125/2.0+top)
    pos.append(pos3)
    pos4=large_frame(l_center,b_center,PA_deg, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm, left=-0.125+left,top=0.125/2.0+top)
    pos.append(pos4)

    return pos

def inout_fillgap_large_frame(targets, fillgap_large_convexes):
    """inout fill gap dithering 

    Args:
        targets: targets
        fillgap_large_convex: fillgap_large_convex

    Returns:
        inout mask sequence of inout mask of four detectors (in = 1 or out = 0 mask), (3,4,N)
    """
    ans=[]
    for large_convex in fillgap_large_convexes:
        a=inout_large_frame(targets,large_convex)
        ans.append(a)
    return ans

