import feistel_cipher

# tasks 1+2 perform encryption and decryption of a plaintext, 
# using linear round function
def main():
    rounds = 17
    msg_l = 32
    linear_rf = 1 # linear round function flag

    text = "{0:032b}".format(0x80000000)    # Insert String
    key = "{0:032b}".format(0x80000000)     # Insert key

    x = feistel_cipher.encryption(text, key, msg_l, rounds, linear_rf)
    print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", Key: " + str(hex(int(key, 2))) + "\nCiphertext: " + str(hex(int(x, 2))))
    u = feistel_cipher.decryption(x, key, msg_l, rounds, linear_rf)
    print("DECRYPTION:\nCiphertext: " + str(hex(int(x , 2))) + ", Key: " + str(hex(int(key, 2))) + "\nPlaintext: " + str(hex(int(u, 2))))

if __name__ == '__main__':
    main()
