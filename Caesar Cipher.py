import string
from collections import Counter

def caesar_encrypt(plaintext, z):
    """Encrypt text using Caesar cipher with specified shift z"""
    z = z % 26
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    
    translation_table = str.maketrans(
        uppercase + lowercase,
        uppercase[z:] + uppercase[:z] + lowercase[z:] + lowercase[:z]
    )
    
    return plaintext.translate(translation_table)

def caesar_decrypt(ciphertext, z):
    """Decrypt Caesar cipher text using the specified shift z"""
    return caesar_encrypt(ciphertext, -z)



def brute_force_caesar(ciphertext):
    """Try all 26 possible shifts"""
    return [(z, caesar_decrypt(ciphertext, z)) for z in range(26)]

def identify_plaintext(decryptions):
    """Identify the most likely correct plaintext"""
    # Common English words
    common_words = ['the', 'and', 'that', 'this', 'have', 'has', 'is', 'for', 'not', 'with', 'you', 'but',
                     'he', 'she', 'they', 'are', 'on', 'at', 'to', 'from', 'by',
                     'was', 'were', 'will', 'would', 'could', 'should', 'it', 'in', 'of', 'a', 'an']
    
    best_score = -1
    best_result = None
    
    for z, text in decryptions:
        # Count common words
        text_lower = text.lower()
        word_score = sum(text_lower.count(' ' + word + ' ') for word in common_words)
        
        # Letter frequency analysis (simplified)
        # English letters from most to least common: etaoinshrdlu
        letters = Counter(c for c in text_lower if c.isalpha()).most_common(6)
        freq_score = sum(1 for l, _ in letters if l in 'etaoin')
        
        # Combined score
        score = word_score + freq_score
        
        if score > best_score:
            best_score = score
            best_result = (z, text)
    
    return best_result



# Example usage
if __name__ == "__main__":
    # Original text and encryption
    original = "meet them after work."
    z = 13  # Our secret key 'z'
    encrypted = caesar_encrypt(original, z)
    
    print(f"Original: {original}")
    print(f"Encrypted (shift={z}): {encrypted}")
    
    # Brute force attack
    print("\nPerforming brute force attack...")
    decryptions = brute_force_caesar(encrypted)
    
    # Identify likely plaintext
    best_z, best_text = identify_plaintext(decryptions)
    
    print(f"\nMost likely plaintext (shift={best_z}):")
    print(best_text)
    
    # Show whether the attack was successful
    print(f"\nAttack successful? {'Yes' if best_z == z else 'No'}")
    print(f"Actual key was: {z}")




