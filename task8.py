import random

rounds = 13
msg_l = 16




def nl_roundf(current_key, current_text):
    # Implementation of the non linear round function

    final_text = ""
    msg_h = int(msg_l/2)    # Half of the length of the message
    
    for j in range(msg_h):
        if (j<msg_h/2):
            final_text += str((int(current_text[j]) & int(current_key[2*(j+1)-2])) | (int(current_text[2*(j+1)-2]) & int(current_key[2*(j+1)-1])) | int(current_key[4*(j+1)-1]))
        else:
            final_text += str((int(current_text[j]) & int(current_key[2*(j+1)-2])) | (int(current_key[4*(j+1)-(msg_l)-2]) & int(current_key[2*(j+1)-1])) | int(current_text[2*(j+1)-(msg_h)-1]))

    return final_text




def keyGen(current_round, key):
    # Given the index of the round (current_round)
    # and the key, returns the subkey for that round
    key_final = ""

    for j in range(msg_l):
        h = ((5*current_round + j) % msg_l)
        key_final += key[h] 
    
    return key_final




def feistel_interaction(u, k, round_index, message_length):
    # Given the input message u and the
    # key k, return a ciphertext x
    # This counts as one round of the cipher

    # Substitution
    y = u[0:int(message_length/2)]   # Left half
    z = u[int(message_length/2):int(message_length)]    # Right half
    w = nl_roundf(k, y)

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
    
    
    
    
# Function to create the random key (as a binary string) 
def rand_key(p): 
    key = "" 
    #generate random key string of length p
    for i in range(p): 
        temp = str(random.randint(0, 1)) 
        key += temp 
          
    return(key)




#quicksort algorithm (keys array is rearranged according to how ciphers are sorted)
def quick_sort(array, keys, start, end):
    if start >= end:
        return

    p = partition(array, keys, start, end)
    quick_sort(array, keys, start, p-1)
    quick_sort(array, keys, p+1, end)




#support function for quicksort
def partition(array, keys, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        # If the current value we're looking at is larger than the pivot
        # it's in the right place (right side of pivot) and we can move left,
        # to the next element.
        # We also need to make sure we haven't surpassed the low pointer, since that
        # indicates we have already moved all the elements to their correct side of the pivot
        while low <= high and array[high] >= pivot:
            high = high - 1

        # Opposite process of the one above
        while low <= high and array[low] <= pivot:
            low = low + 1

        # We either found a value for both high and low that is out of order
        # or low is higher than high, in which case we exit the loop
        if low <= high:
            array[low], array[high] = array[high], array[low]
            keys[low], keys[high] = keys[high], keys[low]
            # The loop continues
        else:
            # We exit out of the loop
            break

    array[start], array[high] = array[high], array[start]
    keys[start], keys[high] = keys[high], keys[start]

    return high




# support function for this program that looks for matches 
# between the two tables of "intermediate" plaintexts and ciphertexts
#
# when a match is found the relative keys that produced it are stored to be later returned

def search_matches(cipher, key1, plain, key2, N):
    final_keys = [[],[]]
    
    i, j, k = 0, 0, 0
    
    while i<N and j<N:
        if cipher[i]< plain[j]:
            i+=1
        elif plain[j]< cipher[i]:
            j+=1
        else:
            #found a match between x' and u'' !, save the correponding key values
            final_keys[0].append(key1[i])
            final_keys[1].append(key2[j])
            j+=1
            i+=1
        
    return final_keys




def main():
    N = 10000

    #initialise empty arrays
    key1_guess = [None]*N
    key2_guess = [None]*N
    cipher_guess = [None]*N
    plain_guess = [None]*N
    plaintext = ["1010011110110100", "0010100110100000", "0001111001110110", "0111111110010100", "1111010110110001"]
    ciphertext = ["1001100100010101", "1111010110001111", "0010011100110010", "1111101111010001", "1011100001100000"]
    
    # generate N random key1 guesses, 
    # and compute corrresponding cipher guess for each
    #(use 1st plpaintext)
    print("generating key1s and encrypting plaintext...")
    for i in range(N):
        key1_guess[i] = rand_key(16)
        cipher_guess[i] = encryption(plaintext[0], key1_guess[i])
        
    print("DONE!\n\nsorting by cipher...")
    
    
    #sort by cipher_guess value
    quick_sort(cipher_guess, key1_guess, 0, N-1)    
    print("DONE!\n\ngenerating key2s and decrypting ciphertext...")
    
    
    # generate N random key2 guesses, 
    # and compute corrresponding plaintext guess for each
    #(use 1st cipher)
    for i in range(N):
        key2_guess[i] = rand_key(16)
        plain_guess[i] = decryption(ciphertext[0], key2_guess[i])
        #print(plain_guess[i], key2_guess[i])
    
    print("DONE!\n\nsorting by plaintext...")
     
    
    #sort by plain_guess value
    quick_sort(plain_guess, key2_guess, 0, N-1)    
    print("DONE!\n\nlooking for matches...")
    
    #look for matches between the two tables of ciphers and plaintexts
    final_keys = search_matches(cipher_guess, key1_guess, plain_guess, key2_guess, N)

    if len(final_keys[0]) != 0:
        #we found some matches
        
        print("DONE!\nORIGINAL CIPHERTEXT:", ciphertext[0], "\n")
        
        for i in range(len(final_keys)):
            print("keys:", final_keys[0][i],final_keys[1][i])
            
            epic = encryption(encryption(plaintext[0], final_keys[0][i]), final_keys[1][i])
            print("guessed ciphertext:",epic)
            
            if(epic == ciphertext[0]):
                print("CORRECT GUESS, THE ATTACK WAS SUCCESSFUL!!!\n")
    else:
        print("NO MATCHES!")
        
        
        
        
if __name__ == '__main__':
    main()