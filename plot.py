import matplotlib.pyplot as plt
from numpy import pi, sqrt, cos, arange, sin, exp, array  #


def get_T_prev(n, nlast, angle, n_prev, n_next):

    kx = nlast * sin(angle)

    def kzi(ni):
        kzi = sqrt(ni ^ 2 - kx ^ 2)
        return kzi

    # TE POLARISATION
    r_prev = (kzi(n_prev) - kzi(n))/(kzi(n_prev) + kzi(n))
    r = (kzi(n) - kzi(n_next))/(kzi(n) + kzi(n_next))
    t = 2*kzi(n_prev)/(kzi(n_prev) + kzi(n))
    t_prev = 2*kzi(n)/(kzi(n) + kzi(n_next))

    Tprev=[[0,0],[0,0]]
    Tprev[0][0]=(t_prev*t-r*r_prev)/(t)
    Tprev[0][1]=r/(t)
    Tprev[1][0]=(-1)*r_prev/(t)
    Tprev[1][1]=1/(t)
    return array(Tprev)


def get_T(i,h, nlast, angle,n, lamb):
    kx = nlast * sin(angle)

    def kzi(ni):
        kzi = sqrt(ni ^ 2 - kx ^ 2)
        return kzi

    T=[[0, 0], [0, 0]]
    T[0][0]=exp(2*pi()*i*kzi(n)/lamb)
    T[0][1]=0
    T[1][0]=0
    T[1][1]=exp((-1)*2*pi()*i*kzi(n)/lamb)
    return array(T)

def get_last_t(i, ni,nlast, ni_prev, ni_next, lambi, hi, angle):
        Ti=get_T_prev(ni,nlast,angle,ni_prev,ni_next).dot(get_T(i,hi,nlast,angle,ni,lambi))
        return Ti
