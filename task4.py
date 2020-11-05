import numpy

def split_string(s):
    split=[]
    for i in range(0, len(s), 1):
        split.append(s[i])
    return split

def inverse_matrix(mtx):
    return 1-mtx

def find_key(x,u,invA,B):
    # computing B*u
    Bu=[]
    for i in range(len(B)):
        for j in range(len(B)):
            if (j==0):
                Bu.append(B[i][j]*u[j])
            else:
                Bu[i]=Bu[i]+(B[i][j]*u[j])
    # adding x to Bu
    xBu=[]
    for i in range(len(x)):
        xBu.append(x[i]+Bu[i])
    # computing k
    k=[]
    for i in range(len(invA)):
        for j in range(len(invA)):
            if (j==0):
                k.append(invA[i][j]*x[j])
            else:
                k[i]=k[i]+(invA[i][j]*x[j])
    return k

def main():
    matrixA = numpy.fromfile('linear_key_output.txt', numpy.int32, -1, ',', 0)
    matrixB = numpy.fromfile('linear_text_output.txt', numpy.int32, -1, ',', 0)
    A = numpy.array(matrixA).reshape((32, 32))
    B = numpy.array(matrixB).reshape((32, 32))
    print("\nThe A matrix is:\n" + str(A) + "\n")
    print("The B matrix is:\n" + str(B) + "\n\n")
    invA = inverse_matrix(A)

    plain1 = "{0:032b}".format(0x08D17555)
    cipher1 = "{0:032b}".format(0x22C74406)
    p1=split_string(plain1)
    c1=split_string(cipher1)
    print("The plaintext1 is:\n"+str(p1))
    print("The ciphertext1 is:\n"+str(c1)+"\n\n")

    plain2 = "{0:032b}".format(0x70518CE4)
    cipher2 = "{0:032b}".format(0xA3F6BDB7)
    p2 = split_string(plain2)
    c2 = split_string(cipher2)
    print("The plaintext2 is:\n" + str(p2))
    print("The ciphertext2 is:\n" + str(c2) + "\n\n")

    plain3 = "{0:032b}".format(0x61ADD0A6)
    cipher3 = "{0:032b}".format(0xEE48E1F5)
    p3 = split_string(plain3)
    c3 = split_string(cipher3)
    print("The plaintext3 is:\n" + str(p3))
    print("The ciphertext3 is:\n" + str(c3) + "\n\n")

    plain4 = "{0:032b}".format(0xC3F8E881)
    cipher4 = "{0:032b}".format(0x743AD9D2)
    p4 = split_string(plain4)
    c4 = split_string(cipher4)
    print("The plaintext4 is:\n" + str(p4))
    print("The ciphertext4 is:\n" + str(c4) + "\n\n")

    plain5 = "{0:032b}".format(0xCB923881)
    cipher5 = "{0:032b}".format(0xAC5009D2)
    p5 = split_string(plain5)
    c5 = split_string(cipher5)
    print("The plaintext5 is:\n" + str(p5))
    print("The ciphertext5 is:\n" + str(c5) + "\n\n")

    k1 = find_key(p1, c1, invA, B)
    print("k1: " + str(k1) + "\n")
    k2 = find_key(p2, c2, invA, B)
    print("k2: " + str(k2) + "\n")
    k3 = find_key(p3, c3, invA, B)
    print("k3: " + str(k3) + "\n")
    k4 = find_key(p4, c4, invA, B)
    print("k4: " + str(k4) + "\n")
    k5 = find_key(p5,c5,invA,B)
    print("k5: " + str(k5)+"\n")

if __name__ == '__main__':
    main()