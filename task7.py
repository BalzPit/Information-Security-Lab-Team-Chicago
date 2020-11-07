import feistel_cipher


# task 7 performs encryption and decryption of a plaintext, 
# using the non linear round function
def main():
    rounds = 13
    msg_l = 16
    non_linear_rf = 3 #flag for usage of the non linear round function

    text = "{0:016b}".format(0x0000) #Insert String
    key = "{0:016b}".format(0x369c) #Insert key
    
    x = feistel_cipher.encryption(text, key, msg_l, rounds, non_linear_rf)
    print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", Key: " + str(hex(int(key, 2))) + "\nCiphertext: " + str(hex(int(x, 2))))
    u = feistel_cipher.decryption(x, key, msg_l, rounds, non_linear_rf)
    print("DECRYPTION:\nCiphertext: " + str(hex(int(x , 2))) + ", Key: " + str(hex(int(key, 2))) + "\nPlaintext: " + str(hex(int(u, 2))))

if __name__ == '__main__':
    main()