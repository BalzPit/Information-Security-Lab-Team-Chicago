# File containing all the support functions that are used to implement 
# the necessary tasks and enable encryption and decryption, 
# such as the different round functions (linear, nearly linear, non linear)
# and other support methods




# Implementation of the linear round function for tasks 1 and 2
def linear_roundf(current_key, current_text, msg_l):

    final_text = ""
    msg_h = int(msg_l/2)    # Half of the length of the message

    for j in range(msg_h):
        if (j<msg_h/2):
            final_text += str(int(current_text[j]) ^ int(current_key[4*(j+1)-4]))
        else:
            final_text += str(int(current_text[j]) ^ int(current_key[4*(j+1)-(msg_l+1)]))

    return final_text




# Implementation of the nearly linear round function for task 5
def nearly_linear_roundf(current_key, current_text, msg_l):

    final_text = ""
    msg_h = int(msg_l/2)    # Half of the length of the message

    for j in range(msg_h):
        if (j<msg_h/2):
            final_text += str(int(current_text[j]) ^ (int(current_key[4*(j+1)-4]) & (int(current_text[2*(j+1)-2]) | int(current_key[2*(j+1)-2]) | int(current_key[2*(j+1)-1]) | int(current_key[4*(j+1)-3]))))
        else:
            final_text += str(int(current_text[j]) ^ (int(current_key[4*(j+1)-(msg_l+1)]) & (int(current_key[4*(j+1)-(msg_l+2)]) | int(current_key[2*(j+1)-2]) | int(current_key[2*(j+1)-1]) | int(current_text[2*(j+1)-(msg_h+1)]))))

    return final_text



# Implementation of the non linear round function for task 7
def non_linear_roundf(current_key, current_text, msg_l):

    final_text = ""
    msg_h = int(msg_l/2)    # Half of the length of the message
    
    for j in range(msg_h):
        if (j<msg_h/2):
            final_text += str((int(current_text[j]) & int(current_key[2*(j+1)-2])) | (int(current_text[2*(j+1)-2]) & int(current_key[2*(j+1)-1])) | int(current_key[4*(j+1)-1]))
        else:
            final_text += str((int(current_text[j]) & int(current_key[2*(j+1)-2])) | (int(current_key[4*(j+1)-(msg_l)-2]) & int(current_key[2*(j+1)-1])) | int(current_text[2*(j+1)-(msg_h)-1]))

    return final_text



    
# Given the index of the round (current_round)
# and the key, returns the subkey for that round
def keyGen(current_round, key, msg_l):
    key_final = ""

    for j in range(msg_l):
        key_final +=  key[((5*current_round + j) % msg_l) ] 
    
    return key_final




# Given the input message u and the
# key k, return a ciphertext x
# This counts as one round of the cipher
def feistel_interaction(u, k, round_index, message_length, rounds, rf):
    # Substitution
    y = u[0:int(message_length/2)]   # Left half
    z = u[int(message_length/2):int(message_length)]    # Right half
    w = ""
    
    #perform round function depending on the value of the flag rf
    if rf == 1:
        w = linear_roundf(k, y, message_length)
    elif rf == 2:
        w = nearly_linear_roundf(k, y, message_length)
    elif rf == 3:
        w = non_linear_roundf(k, y, message_length)

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



#  encryption with the specified round function
def encryption(text, key, msg_l, rounds, rf):
    x = text
    # Every cycle corresponds to an interaction of the algorithm
    for i in range(1, rounds + 1):
        x = feistel_interaction(x, keyGen(i, key, msg_l), i, msg_l, rounds, rf)

    return x




#  decryption with the specified round function
def decryption(x, key, msg_l, rounds, rf):
    for i in range(1, rounds + 1):
        x = feistel_interaction(x, keyGen(rounds + 1 - i, key, msg_l), i, msg_l, rounds, rf)

    return(x)