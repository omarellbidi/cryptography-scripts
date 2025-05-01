import string

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

def known_plaintext_attack(plaintext, ciphertext):

    # Verify that both texts have the same length
    if len(plaintext) != len(ciphertext):
        print("Error: Plaintext and ciphertext must have the same length")
        return None
    
    # Store detected shifts 
    detected_shifts = []
    
    for i in range(len(plaintext)):
        if plaintext[i].isalpha() and ciphertext[i].isalpha():
            # Convert both characters to lowercase for consistent comparison
            p_char = plaintext[i].lower()
            c_char = ciphertext[i].lower()
            
            # Calculate character positions 
            p_val = ord(p_char) - ord('a')
            c_val = ord(c_char) - ord('a')
            
            # Calculate the shift: (ciphertext - plaintext) mod 26
            # This represents how many positions the plaintext was shifted to get the ciphertext
            shift = (c_val - p_val) % 26
            detected_shifts.append(shift)
    
    if not detected_shifts:
        print("Error: No alphabetic characters found for comparison")
        return None
    
    # Verify all detected shifts are consistent
    first_shift = detected_shifts[0]
    if not all(shift == first_shift for shift in detected_shifts):
        print("Warning: Inconsistent shifts detected. This might not be a Caesar cipher.")
        # Return the most common shift value
        from collections import Counter
        most_common_shift = Counter(detected_shifts).most_common(1)[0][0]
        return most_common_shift
    
    return first_shift

# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("ABC", 3), 
        ("Hello World", 7), 
        ("Meet me at midnight", 12),
        ("128!@#", 10)  # no alphabetic characters
    ]
    
    for plaintext, actual_key in test_cases:
        # Encrypt
        ciphertext = caesar_encrypt(plaintext, actual_key)
        
        # Perform known plaintext attack
        detected_key = known_plaintext_attack(plaintext, ciphertext)
        
        # Output results
        print(f"\nPlaintext:  {plaintext}")
        print(f"Ciphertext: {ciphertext}")
        print(f"Actual key: {actual_key}, Detected key: {detected_key}")
        print(f"Attack successful? {'Yes' if detected_key == actual_key else 'No' if detected_key is not None else 'Failed'}")
    
    # Additional test for error handling
    print("\n--- Error Handling Tests ---")
    result = known_plaintext_attack("Hello", "Hi")  # Different lengths
    print(f"Result with different lengths: {result}")
    
    result = known_plaintext_attack("123", "456")  # No alphabetic characters
    print(f"Result with no alphabetic characters: {result}")
