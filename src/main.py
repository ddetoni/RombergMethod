from __future__ import print_function
from numpy import add, isscalar, asarray, arange


def tupleset(t, i, value):
    l = list(t)
    l[i] = value
    return tuple(l)

def romb(y, dx=1.0, axis=-1, show=False):

    y = asarray(y)
    nd = len(y.shape)
    Nsamps = y.shape[axis]
    Ninterv = Nsamps-1
    n = 1
    k = 0
    while n < Ninterv:
        n <<= 1
        k += 1
    if n != Ninterv:
        raise ValueError("Number of samples must be one plus a "
                "non-negative power of 2.")

    R = {}
    all = (slice(None),) * nd
    slice0 = tupleset(all, axis, 0)
    slicem1 = tupleset(all, axis, -1)
    h = Ninterv*asarray(dx)*1.0
    R[(1,1)] = (y[slice0] + y[slicem1])/2.0*h
    slice_R = all
    start = stop = step = Ninterv
    for i in range(2,k+1):
        start >>= 1
        slice_R = tupleset(slice_R, axis, slice(start,stop,step))
        step >>= 1
        R[(i,1)] = 0.5*(R[(i-1,1)] + h*add.reduce(y[slice_R],axis))
        for j in range(2,i+1):
            R[(i,j)] = R[(i,j-1)] + \
                       (R[(i,j-1)]-R[(i-1,j-1)]) / ((1 << (2*(j-1)))-1)
        h = h / 2.0

    if show:
        if not isscalar(R[(1,1)]):
            print("*** Printing table only supported for integrals" +
                  " of a single data set.")
        else:
            try:
                precis = show[0]
            except (TypeError, IndexError):
                precis = 5
            try:
                width = show[1]
            except (TypeError, IndexError):
                width = 8
            formstr = "%" + str(width) + '.' + str(precis)+'f'

            print("\n       Richardson Extrapolation Table for Romberg Integration       ")
            print("====================================================================")
            for i in range(1,k+1):
                for j in range(1,i+1):
                    print(formstr % R[(i,j)], end=' ')
                print()
            print("====================================================================\n")

    return R[(k,k)]


def main():
    a = arange(9)

    for num in a:
        print (num)

    romb(a, show=True)


if __name__ == "__main__":

    main()
