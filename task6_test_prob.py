import random as rn

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

    f = open("output_hex.txt","w")

    for i in range(100000):
        u = rn.randint(0, 2**32 - 1)
        u = "{0:032b}".format(u)
        k = rn.randint(0, 2**32 - 1)
        k = "{0:032b}".format(k)

        x = encryption(u, k)

        u = str(hex(int(u, 2)))
        k = str(hex(int(k, 2)))
        x = str(hex(int(x, 2)))

        f.write(u[2:] + "," + k[2:] + "," + x[2:])
        f.write("\n")

    f.close()
        

if __name__ == '__main__':
    main()
