from telescope_baseline.mapping.aperture import cos_angle_from_normal_vectorAB, vec2ring, inout_convex_on_sphere, square_convex, inout_single_square_convex, inout_detector
from telescope_baseline.mapping.pixelfunc import vec2ang
import numpy as np
import pytest

def test_cos_angle_from_normal_vectorAB():
    a=np.array([1,0,0])
    b=np.array([0,1,0])
    v=cos_angle_from_normal_vectorAB(a,b,[ np.cross(a,b)])
    assert v[0]==1

def test_vec2ring():
    a=np.array([[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]])
    assert np.sum(vec2ring(a)[0,0,:]) == 6*3
    assert np.sum(vec2ring(a)[0,1,:]) == 1*3
    assert np.sum(vec2ring(a)[1,0,:]) == 1*3
    assert np.sum(vec2ring(a)[1,1,:]) == 2*3

def test_inout_convex_on_sphere():
    ex=np.array([1,0,0])
    ey=np.array([0,1,0])
    ea=np.array([0,1.0/np.sqrt(2.0),1.0/np.sqrt(2.0)])
    eb=np.array([1.0/np.sqrt(2.0),0,1])
    v=np.array([ex,ey,ea,eb])
    angv=np.array(vec2ang(v)) # (Nvertex, theta-phi)
    
    w=np.array([0,0,1])
    angw=np.array(vec2ang(w)).T[0] # (Nvertex, theta-phi)
    assert inout_convex_on_sphere(angv,angw)==0

    w=np.array([1/np.sqrt(2.0),1/np.sqrt(2.0),1/np.sqrt(4.0)])
    angw=np.array(vec2ang(w)).T[0] 
    assert inout_convex_on_sphere(angv,angw)==1

def test_inout_convex_on_sphere_map():
    ex=np.array([1,0,0])
    ey=np.array([0,1,0])
    ea=np.array([0,1.0/np.sqrt(2.0),1.0/np.sqrt(2.0)])
    eb=np.array([1.0/np.sqrt(2.0),0,1])
    v=np.array([ex,ey,ea,eb])
    angv=np.array(vec2ang(v)) # (theta-phi, Nvertex)
    
    w=np.array([0,0,1])
    q=np.array([1/np.sqrt(2.0),1/np.sqrt(2.0),1/np.sqrt(4.0)])
    v=np.array([w,q,w,q])
    angw=np.array(vec2ang(v))
    ans=inout_convex_on_sphere(angv,angw)
    assert (np.sum((ans - [0,1,0,1])**2)) == 0


def test_inout_detector():
    import pkg_resources           
    from telescope_baseline.mapping.read_catalog import read_jasmine_targets
    hdf=pkg_resources.resource_filename('telescope_baseline', 'data/cat.hdf')
    targets,l,b, hw=read_jasmine_targets(hdf)
    each_width_mm=19.52
    width_mm=22.4
    EFL_mm=4370.0
    l_center=-0.5
    b_center=0.5
    PA=30.0
    ans=inout_detector(targets,l_center,b_center,PA, width_mm=width_mm, each_width_mm=each_width_mm, EFL_mm=EFL_mm)
    assert np.sum(ans)==2091
    return ans

if __name__=="__main__":
    test_inout_detector()
