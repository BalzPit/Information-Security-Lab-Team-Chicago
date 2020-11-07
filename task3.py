import feistel_cipher

# task 3 calculates matrix A and svaes it into a file 
def main():
    rounds = 17
    msg_l = 32
    linear_rf = 1 #flag for usage of the linear round function
    
    #Calculating A
    text = "{0:032b}".format(0x80000000)   # Insert String
    key = "{0:032b}".format(0x0)    # Insert key
    f = open("linear_text_output.txt","w")

    # Generator of bases for text
    for i in range(32):
        x = feistel_cipher.encryption(text, key, msg_l, rounds, linear_rf)
        print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", + Key: " + str(hex(int(key, 2))) + " --> Ciphertext: " + str(hex(int(x, 2))))
        
        text =  "{0:032b}".format(int(int(text,2)/2)) # Shift of the 1
        for j in x:
            f.write(j +",")
        f.write("\n")
    f.close()

    f = open("linear_key_output.txt","w")
    # Generator of bases for key
    text = "{0:032b}".format(0x0)   # Insert String
    key = "{0:032b}".format(0x80000000)
    for i in range(32):
        x = feistel_cipher.encryption(text, key, msg_l, rounds, linear_rf)
        print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", + Key: " + str(hex(int(key, 2))) + " --> Ciphertext: " + str(hex(int(x, 2))))
        
        key =  "{0:032b}".format(int(int(key,2)/2)) #Shift of the 1
        for j in x:
            f.write(j +",")
        f.write("\n")
    f.close()

if __name__ == '__main__':
    main()
