import matplotlib.pyplot as plt
import numpy as np
from telescope_baseline.mapping.aperture import ang2lb
from matplotlib import patches

def convert_to_convexes(larger_convex):
    """ Convert convexesset, large_convex or larger convex to convexes

    Args:
       larger_convex: convexes set

    Returns:
       convexes (Nconvex, 2, Nvertex)

    """
    pos=np.array(larger_convex)
    shapepos=np.array(np.shape(pos))
    if len(shapepos) > 3:

        Nextra_dimension=len(shapepos)-2
        M=np.prod(shapepos[0:Nextra_dimension])
        pos=pos.reshape((M,2,4))
        return pos
    elif len(shapepos) == 3:
        return pos
    else:
        raise ValueError("larger_convex should be larger than convexes.")




def add_region(pos,ax,autoshift=True,alpha=0.3):
    """plot a patch of detector region on sky

    Args:
       pos: convexes (Nconvex, 2, Nvertex)
       ax: ax for plotting
       autoshift: if True, convert l to -180, 180 deg
       alpha: alpha

    """
    M=np.shape(pos)[0]
    for i in range(M):
        xy=np.array(ang2lb(pos[i,:]))
        if autoshift:
            xy[0]=np.mod(xy[0]+180.0,360.0)-180.0
        xy=xy.T
        patch = patches.Polygon(xy=xy, closed=True,fill=False,ls="--",lw=0.5,color="green",alpha=alpha)
        ax.add_patch(patch)


def plot_targets(l,b,ans,pos=None,outfile="map.png"):
    """plot targets in general

    Args:
       l: l
       b: b
       ans: targets position
       pos: detector position
       outfile: output file name

    """
    
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    ax.plot(l,b,".",alpha=0.03,color="black")
    if len(np.shape(ans))==1:
        ax.plot(l[ans],b[ans],".",alpha=0.1)
        ax.set_title("N in Detector ="+str(len(b[ans]))+" Hw<12.5")
    else:
        for ans_each in ans:
            ax.plot(l[ans_each],b[ans_each],".",alpha=0.05,color="C3")
    if pos is not None:
        add_region(pos,ax)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

def plot_n_targets(l,b,nans,pos=None,outfile="nmap.png",cmap="CMRmap"):
    """plot number of targets 

    Args:
       l: l
       b: b
       nans: number of observations for targets
       pos: detector position
       outfile: output file name
       cmap: colormap
    """

    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9,cmap=cmap)
    if pos is not None:
        add_region(pos,ax)
    ax.set_facecolor('gray')
    labels(cb,outfile,ax)

def plot_ae_targets(l,b,nans,pos=None,outfile="aemap.png",cmap="CMRmap",vmax=50.0):
    """plot astrometric errors targets 

    Args:
       l: l
       b: b
       nans: number of observations for targets
       pos: detector position
       outfile: output file name
       cmap: colormap
       vmax: colorbar max value
    """
    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    cb=ax.scatter(l,b,s=1,c=nans,alpha=0.9, cmap=cmap, vmax=vmax)
    if pos is not None:
        add_region(pos,ax)
    ax.set_facecolor('black')
    labels(cb,outfile,ax)

def labels(cb,outfile,ax):
    """put label

    Args:
       cb: colorbar
       outfile: output file name
       ax: ax

    """
    plt.colorbar(cb,shrink=0.5)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()

    
def hist_n_targets(nans,scale=1.0,outfile="nhist.png"):
    """plot histogram of N of targets

    Args:
       nans: number array
       scale: scale
       outfile: output file name

    """
    nans=nans[nans>0]
    orign=int(np.max(nans))
    nans=nans*scale
    fig=plt.figure()
    ax=fig.add_subplot(111)
    cb=ax.hist(nans, bins=orign, alpha=0.5, ec='navy', range=(0.5*scale, np.max(nans)+0.5*scale))
    ax.set_xlabel("N")
    ax.set_ylabel("number of the targets")
    plt.savefig(outfile)        
    plt.show()

def hist_ae_targets(final_ac,outfile="fac.png"):
    """plot histogram of astrometric errors of targets

    Args:
       final_ac: number array
       outfile: output file name

    """

    fig=plt.figure()    
    ax=fig.add_subplot(111)
    cb=ax.hist(final_ac[final_ac<100.0], alpha=0.5, bins=25, ec='navy')
    ax.set_ylabel("number of targets")
    ax.set_xlabel("final accuracy [umas]")
    plt.savefig(outfile)        
    plt.show()


def plot_convexes(l,b,pos,outfile="pos.png"):
    """plot convexes

    Args:
       l: l
       b: b
       convexes: convexes
    """

    fig=plt.figure()
    ax=fig.add_subplot(111,aspect=1.0)
    ax.plot(l,b,".",alpha=0.01,color="gray")
    add_region(pos,ax,alpha=0.7)
    ax.set_xlabel("l (deg)")
    ax.set_ylabel("b (deg)")
    plt.gca().invert_xaxis()
    plt.savefig(outfile)        
    plt.show()
