import matplotlib.pyplot as plt
import numpy
from numpy import pi, sqrt, cos, arange, sin, exp, array, absolute, real  #


def calc_TE_pol(n, nl, angle, h, wl, n_pod, n_air, polarisation):
    global T01

    def get_T_prev(n, n_pod, angle, n_prev, n_next):
        global r_prev, t_prev, t, r
        kx = n_pod * sin(angle)

        def kzi(ni):
            kzi = numpy.sqrt(ni ** 2 - kx ** 2)
            return kzi

        if polarisation == 'TE':
            r_prev = (kzi(n_prev) - kzi(n)) / (kzi(n_prev) + kzi(n))
            r = (kzi(n) - kzi(n_next)) / (kzi(n) + kzi(n_next))
            t = 2 * kzi(n_prev) / (kzi(n_prev) + kzi(n))
            t_prev = 2 * kzi(n) / (kzi(n) + kzi(n_next))
        elif polarisation == 'TM':
            # #TM POLARISATION
            def Ei(ni):
                Ei = ni ** 2
                return Ei

            r_prev = (Ei(n) * kzi(n_prev) - Ei(n_prev) * kzi(n)) / (Ei(n) * kzi(n_prev) + Ei(n_prev) * kzi(n))
            r = (Ei(n_next) * kzi(n) - Ei(n) * kzi(n_next)) / (Ei(n_next) * kzi(n) + Ei(n) * kzi(n_next))
            t = 2 * Ei(n) * kzi(n_prev) / Ei(n) * (kzi(n_prev) + Ei(n_prev) * kzi(n))
            t_prev = 2 * Ei(n_next) * kzi(n) / (Ei(n_next) * kzi(n) + Ei(n) * kzi(n_next))

        Tprev = [[0, 0], [0, 0]]
        Tprev[0][0] = (t_prev * t - r * r_prev) / t_prev
        Tprev[0][1] = r / t_prev
        Tprev[1][0] = (-1) * r_prev / t_prev
        Tprev[1][1] = 1 / t_prev
        return array(Tprev)

    def get_T(h, n_pod, angle, n, lamb):
        kx = n_pod * sin(angle)

        # должно быть n_0 sin angle, angle = sup
        def kzi(ni):
            kzi = numpy.sqrt(ni ** 2 - kx ** 2)
            return kzi

        # lamb - длина волны
        T = [[0, 0], [0, 0]]
        T[0][0] = exp((2 * pi * (0 + 1j) * kzi(n) * h * 10 ** (-6)) / (lamb * 10 ** (-6)))
        T[0][1] = 0
        T[1][0] = 0
        T[1][1] = exp((-1) * 2 * pi * (0 + 1j) * kzi(n) * h * 10 ** (-6) / (lamb * 10 ** (-6)))
        return array(T)

    if n == 0:
        T01 = get_T_prev(nl[0], n_pod, angle, n_pod, n_air)
        T01 = T01.dot(get_T(h[0], n_pod, angle, nl[0], wl))
        T01 = T01.dot(get_T_prev(n_air, n_pod, angle, nl[0], n_air))
    else:
        T01 = get_T_prev(nl[0], n_pod, angle, n_pod, nl[1])
        T01 = T01.dot(get_T(h[0], n_pod, angle, nl[0], wl))
        for i in range(1, n):
            T01 = T01.dot(get_T_prev(nl[i], n_pod, angle, nl[i - 1], nl[i + 1]))
            T01 = T01.dot(get_T(h[i], n_pod, angle, nl[i], wl))
        T01 = T01.dot(get_T_prev(nl[-1], n_pod, angle, nl[-2], n_air))
    tau0N = 1 / T01[1][1]  # луч идет сверху
    r00 = -T01[1][0] / T01[1][1]
    rnn = T01[0][1] / T01[1][1]
    tauN_0 = T01[0][0] + (r00 * rnn) / tau0N  # луч идет снизу
    # POWER REFLECTION
    R00 = absolute(r00) ** 2
    RNN = absolute(rnn) ** 2
    # POWER TRANSMISSION FOR TE:
    kz0 = numpy.sqrt(n_air ** 2 - (n_pod * sin(angle)) ** 2)
    kzN1 = numpy.sqrt(n_pod ** 2 - (n_pod * sin(angle)) ** 2)
    if polarisation == 'TE':
        TBIG_0N = (absolute(tau0N) ** 2) * real(kz0 / kzN1)
        TBIG_N0 = (absolute(tauN_0) ** 2) * real(kzN1 / kz0)
    elif polarisation == 'TM':
        E_0 = n_air ** 2
        E_N = n_pod ** 2
        TBIG_0N = (absolute(tau0N) ** 2) * real((kz0 * E_N) / (kzN1 * E_0))
        TBIG_N0 = (absolute(tauN_0) ** 2) * real((kzN1 * E_0) / (kz0 * E_N))
    return R00, RNN, TBIG_0N, TBIG_N0
