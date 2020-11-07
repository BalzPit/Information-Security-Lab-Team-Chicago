import feistel_cipher

# task 5 performs encryption and decryption of a plaintext, 
# using the nearly linear round function
def main():
    rounds = 5
    msg_l = 32
    nearly_linear_rf = 2 #flag for usage of the nearly linear round function
    
    text = "{0:032b}".format(0x12345678)   # Insert String
    key = "{0:032b}".format(0x87654321)    # Insert key

    x = feistel_cipher.encryption(text, key, msg_l, rounds, nearly_linear_rf)
    print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", Key: " + str(hex(int(key, 2))) + "\nCiphertext: " + str(hex(int(x, 2))))
    u = feistel_cipher.decryption(x, key, msg_l, rounds, nearly_linear_rf)
    print("DECRYPTION:\nCiphertext: " + str(hex(int(x , 2))) + ", Key: " + str(hex(int(key, 2))) + "\nPlaintext: " + str(hex(int(u, 2))))

if __name__ == '__main__':
    main()