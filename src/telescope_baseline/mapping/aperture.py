import numpy as np
from telescope_baseline.mapping.pixelfunc import ang2vec, vec2ang


def lb2ang(l,b):
    """convert l and b to ang (theta in radian, phi in radian)
    Args:
       l: galactic coordinate l
       b: galactic coordinate b
    Returns:
       ang (co-latitude=theta in radian, longitude=phi in radian)

    """
    phi=l/180.0*np.pi
    theta=np.pi/2.0-b/180.0*np.pi
    return np.array([theta,phi])

def ang2lb(ang):
    """convert ang (theta in radian, phi in radian) to l and b 
    Args:
       ang (co-latitude=theta in radian, longitude=phi in radian)
    Returns:
       l: galactic coordinate l
       b: galactic coordinate b

    """
    theta, phi=ang
    l=phi*180.0/np.pi
    b=90.0 - theta*180.0/np.pi
    return l, b
    
def basic_convex(center,PA,width,anglist,scale):
    """compute a single convex
    Args: 
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
        anglist: angular position list of the convex
        scale: scale of convex
    Returns:
        detecter convex (ang)
    
    """
    
    thetac,phic=center
    ez=np.array([0.0,0.0,1.0])
    half_diagonal_angle=width*scale
    e0=Roty(half_diagonal_angle)@ez
    convex0=[]
    for ang in anglist:
        convex0.append(Rotz(ang)@e0)
    convex0=np.array(convex0)
    C=np.einsum('ij,kj->ki',Rotz(PA),convex0)
    C=np.einsum('ij,kj->ki',Roty(thetac),C)
    C=np.einsum('ij,kj->ki',Rotz(phic),C)
    Cang = vec2ang(C)
    return np.array(Cang)

def square_convex(center,PA,width):
    """compute a single square convex
    Args: 
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        detecter convex (ang)
    
    """
    anglist=[-3.0*np.pi/4.0,-np.pi/4.0,np.pi/4.0,3.0*np.pi/4.0]
    scale=1.0/np.sqrt(2.0)
    return basic_convex(center,PA,width,anglist,scale)

def ang_detector_unit(direction,scale,center,PA,width):
    """compute a relative ang position in the unit of the detectir size from the original position center/PA/width
    Args: 
        direction: TBLR =top,bottom,left,right
        scale: scale in the detector one side unit
        center: theta, phi of the center
        PA: position angle of the detector (north up)
        width: detector width in radian
    Returns:
        ang (theta, phi)
    
    """

    anglist=[-np.pi/2.0,0.0,np.pi/2.0,np.pi]
    dic={"R":0,"B":1,"L":2,"T":3}
    bc=basic_convex(center,PA,width,anglist,2*scale)
    i=dic[direction]
    return bc[:,i]
    
def lb_detector_unit(direction,scale,l_center,b_center, PA_deg, width_mm=22.4, EFL_mm=4370.0):
    """compute a relative l,b position in the unit of the detectir size from the original position center/PA/width
    Args: 
        direction: TBLR =top,bottom,left,right
        scale: scale in the detector one side unit
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        EFL_mm: effective focal length in the unit of mm
    Returns:
        l,b
    
    """
    PA=PA_deg/180.0*np.pi

    return ang2lb(ang_detector_unit(direction,scale,lb2ang(l_center,b_center),PA,width_mm/EFL_mm))
    
def Roty(theta):
    return np.array([[np.cos(theta),0.0,np.sin(theta)],[0.0,1.0,0.0],[-np.sin(theta),0.0,np.cos(theta)]])

def Rotz(theta):
    return np.array([[np.cos(theta),-np.sin(theta),0.0],[np.sin(theta),np.cos(theta),0.0],[0.0,0.0,1.0]])

def vec2ring(x):
    """convert a vector to a ring
    Args:
        vertex list (vertex, coodinate)

    Returns:
        ring (edge, left-right, coordinate)

    """
    Nvertex, Ncoordinate=np.shape(x)
    if Nvertex%2 == 1:
        raise ValueError("Nvertex needs to be even.")
    rs=(int(Nvertex/2),2,Ncoordinate)
    x1=x.reshape(rs) 
    x0=np.roll(x,1,axis=0).reshape(rs)
    return np.hstack([x0,x1]).reshape((Nvertex,2,Ncoordinate))

def cos_angle_from_normal_vectorAB(a,b,x):
    """cos angle between the normal vector defined by a, b and x
    Args:
       a: 3D vetcor of A, (3,) or (N, 3)
       b: 3D vector of B, (3,) or (N, 3)
       x: vectors whose cos angle from normal vector of the ABO plane to be computed 3 or (M, 3)
     
    Returns:
       cos_angles, float or (N,M)
    """
    return (x@np.cross(a,b).T).T


def inout_convex_on_sphere(convex_ang,target_ang):
    """checking if the target points  are in or out of convex 
    Args:
        convex_ang: list of theta,phi points that defines the convex on a sphere
        target_ang: theta,phi target lists in or out of the convex on a sphere

    Returns:
        1 (in convex) or 0 (out of convex)
    """
    v=ang2vec(convex_ang[0],convex_ang[1])
    w=ang2vec(target_ang[0],target_ang[1])
    Nvertex,Ncoordinate=np.shape(v)
    ring=vec2ring(v)
    cosa=cos_angle_from_normal_vectorAB(ring[:,0,:],ring[:,1,:],w)
    mask=(cosa>=0.0)*(cosa<=1.0)
    return np.prod(mask,axis=0)

def inout_single_square_convex(targets,center,PA,width):
    """checking if targets are in or out single square convex
    
    Args:
        center: theta, phi of the center in radian
        PA: position angle in radian
        width: square width

    Returns:
        inout mask of four detectors (in = 1 or out = 0 mask)
    """
    convex=square_convex(center,PA,width)
    ans=inout_convex_on_sphere(convex,targets)
    ans=np.array(ans,dtype=np.bool_)
    return ans

def four_square_convexes(center,PA,width,each_width):
    """make four square convexes
    
    Args:
        center: theta, phi of the center in radian
        PA: position angle in radian
        width: the separation of squares
        each_width: square width

    Returns:
        convexes: convex positions 
    """    
    convex=square_convex(center,PA,width)
    convex=np.array(convex)
    convexes=[]
    for i in range(0,4):
        each_convex=square_convex(convex[:,i],PA,each_width)
        convexes.append(each_convex)
    return convexes


def inout_four_square_convexes(targets, convexes):
    """checking if targets are in or out four square convexes
    
    Args:
        targets: targets ang position list
        convexes: convexes

    Returns:
        answer: inout mask of four detectors (in = 1 or out = 0 mask) (N,)
    """    
    Ntarget=np.shape(targets)[1]
    answers=np.zeros(Ntarget,dtype=np.bool_)
    for each_convex in convexes:
        ans=inout_convex_on_sphere(each_convex,targets)        
        ans=np.array(ans,dtype=np.bool_)
        answers = answers + ans
    #print(np.shape(answers), "four detector")
    return answers

def inout_detector(targets,l_center,b_center,PA_deg, width_mm=22.4, each_width_mm=19.52,  EFL_mm=4370.0):
    """checking if targets are in or out four square convexes
    
    Args:
        targets: targets
        l_center: center of galactic coordinate, l (deg)
        b_center: center of galactic coordinate, b (deg)
        PA_deg: position angle in deg
        width_mm: the separation of detector chips
        each_width_mm: the chip width in the unit of mm
        EFL_mm: effective focal length in the unit of mm
    Returns:
        answer: inout mask of four detectors (in = 1 or out = 0 mask)
        convexes: convex positions 

    """
    center=lb2ang(l_center,b_center)
    PA=PA_deg/180.0*np.pi
    convexes=four_square_convexes(center,PA,width_mm/EFL_mm, each_width_mm/EFL_mm)
    return inout_four_square_convexes(targets, convexes)

