import numpy

def inverse_matrix(mtx):
    numpy.linalg.inv(mtx)
    return mtx

def find_key(x, u, A, B):
    invA = inverse_matrix(A)
    k = invA * (x + (B * u))

    return k

def main():
    plain1 = "{0:032b}".format(0x08D17555)
    cipher1 = "{0:032b}".format(0x22C74406)
    A = numpy.loadtxt('linear_key_output.txt', delimiter=",")
    B = numpy.loadtxt('linear_text_output.txt', delimiter=",")

    k1 = find_key(plain1, cipher1, A, B)
    print("The first key is: " + str(hex(int(k1, 2))))

if __name__ == '__main__':
    main()