import collections

def xor_encrypt(plaintext, key):
    # Convert text and key to byte arrays
    plaintext_bytes = plaintext.encode('ascii')
    key_bytes = key.encode('ascii')
    
    # Create result buffer
    result = bytearray(len(plaintext_bytes))
    
    # XOR each byte with corresponding key byte
    for i in range(len(plaintext_bytes)):
        result[i] = plaintext_bytes[i] ^ key_bytes[i % len(key_bytes)]
    
    return bytes(result)

def hamming_distance(bytes1, bytes2):
    # XOR bytes and count 1 bits in result
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(bytes1, bytes2))

def find_key_length(ciphertext, max_length=40):
    # Try different key lengths and calculate normalized Hamming distance
    results = {}
    
    for key_length in range(2, min(max_length, len(ciphertext)//2)):
        # Create blocks of key_length
        blocks = [ciphertext[i:i+key_length] for i in range(0, len(ciphertext)-key_length, key_length)]
        
        # Calculate average Hamming distance between consecutive blocks
        total_distance = 0
        pairs = 0
        
        for i in range(len(blocks)-1):
            # Ensure blocks are of equal length for comparison
            if len(blocks[i]) == len(blocks[i+1]) == key_length:
                distance = hamming_distance(blocks[i], blocks[i+1])
                total_distance += distance
                pairs += 1
        
        # Normalize by key length 
        if pairs > 0:
            normalized_distance = (total_distance / pairs) / key_length
            results[key_length] = normalized_distance
    
    # Sort by normalized distance (lowest is most likely)
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    return sorted_results[:3]  # Return top 3 candidates

def find_repeated_sequences(ciphertext, min_length=3):
    distances = []
    
    # Check sequences of different lengths
    for length in range(min_length, 12):  # Limit to reasonable lengths
        # Dictionary to store sequence positions
        sequence_positions = {}
        
        # Find all sequences of the current length
        for i in range(len(ciphertext) - length + 1):
            sequence = ciphertext[i:i+length]
            
            # If sequence seen before, calculate distance
            if sequence in sequence_positions:
                for pos in sequence_positions[sequence]:
                    distances.append(i - pos)
                sequence_positions[sequence].append(i)
            else:
                sequence_positions[sequence] = [i]
    
    return distances

def find_key_length_kasiski(ciphertext):
    # Get distances between repeated sequences
    distances = find_repeated_sequences(ciphertext)
    
    if not distances:
        return []
    
    # Count factors of each distance
    factors = []
    for distance in distances:
        for i in range(2, min(40, distance + 1)):
            if distance % i == 0:
                factors.append(i)
    
    # Return most common factors
    factor_counts = collections.Counter(factors)
    return factor_counts.most_common(3)  # Return top 3 candidates

# Example usage
if __name__ == "__main__":
    
    plaintext = "This is a test message for XOR encryption. The system must detect key length automatically"
    
    # Test different keys to demonstrate key length detection
    for key in ["SECRET", "TESTKEY", "XOR"]:
        print(f"\nTesting with key: '{key}' (length: {len(key)})")
        encrypted = xor_encrypt(plaintext, key)
        
        # Find key length using Hamming distance method
        print("Key length candidates (Hamming method):")
        key_lengths = find_key_length(encrypted)
        for length, score in key_lengths:
            print(f"  Length {length}: score {score:.4f}")
        
        # Find key length using Kasiski method
        print("Key length candidates (Kasiski method):")
        kasiski_results = find_key_length_kasiski(encrypted)
        for length, count in kasiski_results:
            print(f"  Length {length}: occurred {count} times")
