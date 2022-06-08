import matplotlib.pyplot as plt
import numpy
from numpy import pi, sqrt, cos, arange, sin, exp, array, absolute, real  #
#нулевой слой - воздух, n+1 - подложка, самый нижний слой, угол на вход - угол sup
#угол выхода - n+1 слой sub
def calc_TE_pol(n, nl, angle, h, wl, n_pod, n_air):
    global T01

    def get_T_prev(n, n0, angle, n_prev, n_next):

        kx = n0 * sin(angle)
    #должно быть n_0 sin angle, angle = sup

        def kzi(ni):
            kzi = numpy.sqrt(ni ** 2 - kx ** 2)
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


    def get_T(h, n0, angle,n, lamb):
        kx = n0 * sin(angle)

        # должно быть n_0 sin angle, angle = sup
        def kzi(ni):
            kzi = numpy.sqrt(ni ** 2 - kx ** 2)
            return kzi
    #lamb - длина волны
        T=[[0, 0], [0, 0]]
        T[0][0]=exp(2*pi*(0+1j)*kzi(n)*h/lamb)
        T[0][1]=0
        T[1][0]=0
        T[1][1]=exp((-1)*2*pi*(0+1j)*kzi(n)*h/lamb)
        return array(T)

    if n==0:
        T01=get_T_prev(nl[0], n_air, angle, n_air, n_pod)
        T01=T01.dot(get_T(h[0],n_air,angle,nl[0],wl))
        T01=T01.dot(get_T_prev(n_pod,n_air,angle,nl[0],n_pod))
    else:
        T01=get_T_prev(nl[0],n_air,angle,n_air,nl[1])
        T01=T01.dot(get_T(h[0],n_air,angle,nl[0],wl))
        for i in range (1, n):
            T01 = T01.dot(get_T_prev(nl[i], n_air, angle, nl[i - 1], nl[i + 1]))
            T01 = T01.dot(get_T(h[i],n_air,angle,nl[i],wl))
        T01 = T01.dot(get_T_prev(nl[-1], n_air, angle, nl[-2], n_pod))
    tau0N=1/T01[1][1]
    r00=-T01[1][0]/T01[1][1]
    rnn=T01[0][1]/T01[1][1]
    tauN_0=T01[0][0]+(r00*rnn)/tau0N
    R00=absolute(r00)**2
    RNN=absolute(rnn)**2
    kz0=numpy.sqrt(n_air**2 - (n_air*sin(angle))**2)
    kzN1=numpy.sqrt(n_pod**2 - (n_air*sin(angle))**2)
    TBIG_0N=(absolute(tau0N)**2)*real(kz0/kzN1)
    TBIG_N0=(absolute(tauN_0)**2)*real(kzN1/kz0)
    return R00, RNN, TBIG_0N, TBIG_N0