rounds = 17
msg_l = 32

def roundf(current_key, current_text):
    # Implementation of the round function

    final_text = ""
    msg_h = int(msg_l/2)    # Half of the length of the message

    for j in range(msg_h):
        if (j<msg_h/2):
            final_text += str(int(current_text[j]) ^ int(current_key[4*(j+1)-4]))
        else:
            final_text += str(int(current_text[j]) ^ int(current_key[4*(j+1)-(msg_l+1)]))

    return final_text
    

def keyGen(current_round, key):
    # Given the index of the round (current_round)
    # and the key, returns the subkey for that round
    key_final = ""

    for j in range(msg_l):
        key_final +=  key[((5*current_round + j) % msg_l) ] 
    
    return key_final

def feistel_interaction(u, k, round_index, message_length):
    # Given the input message u and the
    # key k, return a ciphertext x
    # This counts as one round of the cipher

    # Substitution
    y = u[0:int(message_length/2)]   # Left half
    z = u[int(message_length/2):int(message_length)]    # Right half
    w = roundf(k, y)

    # Linear transformation
    v = ""
    for i in range(len(z)):
        v += str(int(z[i]) ^ int(w[i]))

    # Transposition
    if round_index < rounds:
        x = v + y
    else:
        x = y + v
    
    return x

def encryption(text, key):
    x = text
    # Every cycle corresponds to an interaction of the algorithm
    for i in range(1, rounds + 1):
        x = feistel_interaction(x, keyGen(i, key), i, msg_l)

    return x

def decryption(x, key):
    for i in range(1, rounds + 1):
        x = feistel_interaction(x, keyGen(rounds + 1 - i, key), i, msg_l)

    return(x)

def main():
    text = "{0:032b}".format(0x80000000)    # Insert String
    key = "{0:032b}".format(0x80000000)     # Insert key

    x = encryption(text, key)
    print("ENCYPTION:\nPlaintext: " + str(hex(int(text, 2))) + ", Key: " + str(hex(int(key, 2))) + "\nCiphertext: " + str(hex(int(x, 2))))
    u = decryption(x, key)
    print("DECRYPTION:\nCiphertext: " + str(hex(int(x , 2))) + ", Key: " + str(hex(int(key, 2))) + "\nPlaintext: " + str(hex(int(u, 2))))

if __name__ == '__main__':
    main()
