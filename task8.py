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
    
    
    
    
# Function to create the random keys (as a binary string vector) 
def rand_keys(num, r): 
    keys = [] 
    
    #generate num randnom integers
    random_nums = random.sample(range(r), num)
    
    #generate random key string of length p
    for i in range(num): 
        keys.append("{0:016b}".format(random_nums[i]))
          
    return(keys)




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
    #number of random guesses
    N = 50000  # < 65536

    #initialise empty arrays
    key1_guess = [None]*N
    key2_guess = [None]*N
    cipher_guess = [None]*N
    plain_guess = [None]*N
    plaintext = []
    ciphertext = []
    final_keys1 = []
    final_keys2 = []

    #read plaintext and ciphertexts from file 
    with open('KPApairsChicago_non_linear.hex','r') as file: 
        w = 0
        # reading each line     
        for line in file:     
            # reading each hex         
            for word in line.split(): 
                if w % 2 == 0 :
                    plaintext.append("{0:016b}".format(int(word, 16)))
                else:
                    ciphertext.append("{0:016b}".format(int(word, 16)))
                w += 1
    
        
    # generate N random key1 guesses with values between 0 and (2^16)-1, 
    # and compute corrresponding cipher guess for each
    #(use 1st plpaintext)
    print("generating key1s and encrypting plaintext...")
    
    #list of random keys without duplicates
    key1_guess = rand_keys(N, 65536)
    for i in range(N): 
        cipher_guess[i] = encryption(plaintext[0], key1_guess[i])
        
    print("DONE!\n\nsorting by cipher...")
    
    #sort pairs by cipher_guess value
    quick_sort(cipher_guess, key1_guess, 0, N-1)    
    print("DONE!\n\ngenerating key2s and decrypting ciphertext...")
    
    
    # generate N random key2 guesses with values between 0 and (2^16)-1, 
    # and compute corrresponding plaintext guess for each
    # (use 1st cipher)
    key2_guess = rand_keys(N, 65536)
    for i in range(N):
        plain_guess[i] = decryption(ciphertext[0], key2_guess[i])
    
    print("DONE!\n\nsorting by plaintext...")
     
    #sort pairs by plain_guess value
    quick_sort(plain_guess, key2_guess, 0, N-1)    
    print("DONE!\n\nlooking for matches...")

    
    #look for matches between the two tables of ciphers and plaintexts
    keys = search_matches(cipher_guess, key1_guess, plain_guess, key2_guess, N)
    print("DONE!\n")
    
    quick_sort(keys[0], keys[1], 0, len(keys[0])-1) 

    if len(keys[0]) != 0:
        #we found some matches
        print("found", len(keys[0]), "key pairs that produced matches")
        for i in range(len(keys[0])):
            #print("\nkeys:", hex(int(keys[0][i], 2)), hex(int(keys[1][i], 2)))
            
            # let's see what happens when we use the keys we found 
            # to encrypt and then decrypt all the known plain/ciphertext pairs.
            # Only if keys succesfully encrypt/decrypt all input pairs 
            # will we consider them a good enough guess!
            good = 1
            
            for n in range(len(plaintext)):
                # concatenated encryption
                cipher_guess = encryption(encryption(plaintext[n], keys[0][i]), keys[1][i])
            
                if(cipher_guess == ciphertext[n]):
                    # Correct Cipher!
                    # concatenated decryption
                    plain_guess = decryption(decryption(cipher_guess, keys[1][i]), keys[0][i])
                    
                    if(plain_guess != plaintext[n]):
                        # keys are not good enough-> we don't want to add them to final_keys
                        good = 0
                        break
                else:
                    # keys are not good enough-> we don't want to add them to final_keys
                    good = 0
                    break
            
            # keys worked on all input plain/cipher pairs 
            # without errors -> they are a very good guess!
            if good:
                final_keys1.append(keys[0][i])
                final_keys2.append(keys[1][i])
        
        
        if len(final_keys1) != 0:
            print("\nFINAL KEYS")
            for i in range(len(final_keys1)):
                print(hex(int(final_keys1[i], 2)), hex(int(final_keys2[i], 2)))
        else:
            print("\nDidn't find a key pair that was able to work on all known (u,x) pairs. We don't have a good enough guess.")
            
    else:
        print("NO MATCHES FOUND!")
        
        
        
        
if __name__ == '__main__':
    main()