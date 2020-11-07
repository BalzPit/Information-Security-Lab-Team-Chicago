import feistel_cipher
import random


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



# task 8 requires to implement a “meet-in-the-middle” attack
def main():
    rounds = 13
    msg_l = 16
    non_linear_rf = 3 #flag for usage of the non linear round function
    
    #number of random guesses
    N = 50000  # < 2^16 = 65536

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
        cipher_guess[i] = feistel_cipher.encryption(plaintext[0], key1_guess[i], msg_l, rounds, non_linear_rf)
        
    print("DONE!\n\nsorting by cipher...")
    
    #sort pairs by cipher_guess value
    quick_sort(cipher_guess, key1_guess, 0, N-1)    
    print("DONE!\n\ngenerating key2s and decrypting ciphertext...")
    
    
    # generate N random key2 guesses with values between 0 and (2^16)-1, 
    # and compute corrresponding plaintext guess for each
    # (use 1st cipher)
    key2_guess = rand_keys(N, 65536)
    for i in range(N):
        plain_guess[i] = feistel_cipher.decryption(ciphertext[0], key2_guess[i], msg_l, rounds, non_linear_rf)
    
    print("DONE!\n\nsorting by plaintext...")
     
    #sort pairs by plain_guess value
    quick_sort(plain_guess, key2_guess, 0, N-1)    
    print("DONE!\n\nlooking for matches...")

    
    #look for matches between the two tables of ciphers and plaintexts
    keys = search_matches(cipher_guess, key1_guess, plain_guess, key2_guess, N)
    print("DONE!\n")
    
    #quick_sort(keys[0], keys[1], 0, len(keys[0])-1) 

    if len(keys[0]) != 0:
        #we found some matches
        print("found", len(keys[0]), "key pairs that produced matches, now performing quality check...")
        for i in range(len(keys[0])):
            #print("\nkeys:", hex(int(keys[0][i], 2)), hex(int(keys[1][i], 2)))
            
            # let's see what happens when we use the keys we found 
            # to encrypt and then decrypt all the known plain/ciphertext pairs.
            # Only if keys succesfully encrypt/decrypt all input pairs 
            # will we consider them a good enough guess!
            good = 1
            
            for n in range(len(plaintext)-1):
                # concatenated encryption
                cipher_guess = feistel_cipher.encryption(feistel_cipher.encryption(plaintext[n+1], keys[0][i], msg_l, rounds, non_linear_rf), keys[1][i], msg_l, rounds, non_linear_rf)
            
                if(cipher_guess == ciphertext[n+1]):
                    # Correct Cipher!
                    # concatenated decryption
                    plain_guess = feistel_cipher.decryption(feistel_cipher.decryption(cipher_guess, keys[1][i], msg_l , rounds, non_linear_rf), keys[0][i], msg_l , rounds, non_linear_rf)
                    
                    if(plain_guess != plaintext[n+1]):
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