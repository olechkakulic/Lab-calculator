import matplotlib.pyplot as plt
from numpy import pi, sqrt, cos, arange, sin, exp, array  #
#нулевой слой - воздух, n+1 - подложка, самый нижний слой, угол на вход - угол sup
#угол выхода - n+1 слой sub

def get_T_prev(n, nlast, angle, n_prev, n_next):

    kx = nlast * sin(angle)
#должно быть n_0 sin angle, angle = sup

    def kzi(ni):
        kzi = sqrt(ni ** 2 - kx ** 2)
        return kzi

    # TE POLARISATION
    r_prev = (kzi(n_prev) - kzi(n))/(kzi(n_prev) + kzi(n))
    #r_prev = r(i-1,i-1)
    r = (kzi(n) - kzi(n_next))/(kzi(n) + kzi(n_next))
    #r = r(i,i)
    t = 2*kzi(n_prev)/(kzi(n_prev) + kzi(n))
    #t = t(i,i-1)
    t_prev = 2*kzi(n)/(kzi(n) + kzi(n_next))
    #t_prev = t(i-1,i)

    # #TM POLARISATION
    # def Ei(ni):
    #     Ei = ni ^ 2
    #     return Ei
    # r_prev = (Ei(n)*kzi(n_prev) - Ei(n_prev)*kzi(n))/(Ei(n)*kzi(n_prev) + Ei(n_prev)*kzi(n))
    # # r_prev = r(i-1,i-1)
    # r = (Ei(n_next)*kzi(n) - Ei(n)*kzi(n_next)) /Ei(n_next)(kzi(n) +Ei(n)*kzi(n_next))
    # #r = r(i,i)
    # t = 2 * Ei(n)*kzi(n_prev) /Ei(n)*(kzi(n_prev) +Ei(n_prev)*kzi(n))
    # # t = t(i,i-1)
    # t_prev = 2*Ei(n_next) * kzi(n) /(Ei(n_next)*kzi(n) +Ei(n)*kzi(n_next))
    # # t_prev = t(i-1,i)
    Tprev=[[0,0],[0,0]]
    Tprev[0][0]=(t_prev*t-r*r_prev)/(t)
    Tprev[0][1]=r/(t)
    Tprev[1][0]=(-1)*r_prev/(t)
    Tprev[1][1]=1/(t)
    return array(Tprev)


def get_T(i,h, nlast, angle,n, lamb):
    kx = nlast * sin(angle)

    # должно быть n_0 sin angle, angle = sup
    def kzi(ni):
        kzi = sqrt(ni ** 2 - kx ** 2)
        return kzi
#lamb - длина волны
    T=[[0, 0], [0, 0]]
    T[0][0]=exp(2*pi*i*kzi(n)*h/lamb)
    T[0][1]=0
    T[1][0]=0
    T[1][1]=exp((-1)*2*pi*i*kzi(n)*h/lamb)
    return array(T)

def get_last_t(i, ni,nlast, ni_prev, ni_next, lambi, hi, angle):
        Ti=get_T_prev(ni,nlast,angle,ni_prev,ni_next).dot(get_T(i,hi,nlast,angle,ni,lambi))
        return Ti
#n_last = n_o,
n=[0,1,2,3,4,5,6]
angle=0.345
wl=[0.1404, 0.1447, 0.1489, 0.1532, 0.1575, 0.1618]
nl=[1.0003954468031, 1.000384471176, 1.0003754104638, 1.0003674523406, 1.0003605550249, 1.0003545167348]
h=[0.4, 0.53, 0.54, 0.04, 0.234, 1.23]


T01=get_T_prev(nl[1],nl[-1],angle,nl[0],nl[2])
T01=T01.dot(get_T(1,h[1],nl[-1],angle,nl[1],wl[1]))
for i in range (2, len(n)-1):
    T01 = T01.dot(get_T_prev(nl[i], nl[-1], angle, nl[i - 1], nl[i + 1]))
    T01 = T01.dot(get_T(i,h[i],nl[-1],angle,nl[i],wl[i]))
print(T01)
#из уравнения n_sub*sin