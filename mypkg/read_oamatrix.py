import h5py
import numpy as np


def main() :
    hdf5 = h5py.File("oamatrix.hdf5", 'r')
    print(list(hdf5.keys()))
    print(hdf5["2^3"].value)
    hdf5.close()


if __name__ == '__main__':
    main()
