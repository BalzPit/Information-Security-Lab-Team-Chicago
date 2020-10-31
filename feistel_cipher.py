import numpy as np

def subkey_generation(key, rounds, key_length):
    subkeys = []    # Array that will contain subkeys for every round
    subkey = []     # Array that will contain 0s and 1s for the subkey
    for i in range(1, rounds): # Cycle for every round index
        for j in range(0, key_length - 1):  # Cycle for every bit of the subkey
            subkey.append(key*(((5*i + j - 1) % key_length) + 1))
        subkeys.append(subkey)

    return subkeys

def round_function(k, y, round_index, half_length):
    # Given the subkeys k and the input y
    # return output w

    w = []
    key = k[round_index]
    for i in range(0, half_length - 1):
        if i <= half_length/2 - 1:
            w[i] = y[i] ^ (key*(4*i - 3))
        if i > half_length/2:
            w[i] = y[i] ^ (key*(4*i-2*half_length))

    return w

def feistel_interaction(u, k, round_index, message_length):
    # Given the input message u and the
    # key k, return a ciphertext x
    # This counts as one round of the cipher

    # Substitution
    y = u[0:int(message_length/2 - 1)]   # Left half
    z = u[int(message_length/2):int(message_length-1)]    # Right half
    w = round_function(k, y, round_index, message_length/2)
    # Linear transformation
    v = z ^ w
    # Transposition
    x = [v, y]
    return x

def main():
    l = 32  # Length of everything
    message_length = l
    key_length = l
    rounds = 17 # Number of rounds

    u = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    k = u

    keys = subkey_generation(k, rounds, key_length)
    x = u

    for i in range(rounds):
        x = feistel_interaction(x, keys[i], i, message_length)

    print(x)


if __name__ == '__main__':
    main()