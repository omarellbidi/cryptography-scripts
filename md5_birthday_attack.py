import hashlib
import os
import random

def get_md5(filename):
    with open(filename, "rb") as f:
        content = f.read()
    return hashlib.md5(content).hexdigest(), content

def create_variant(original_file, variant_num):
    with open(original_file, "rb") as f:
        content = bytearray(f.read())
    
    random.seed(variant_num)
    for _ in range(3):
        mod_type = random.randint(0, 2)
        if mod_type == 0:  # Add null byte
            pos = random.randint(0, len(content)-1)
            content.insert(pos, 0)
        elif mod_type == 1:  # Modify whitespace
            spaces = [i for i, byte in enumerate(content) if byte == ord(' ')]
            if spaces:
                pos = random.choice(spaces)
                if random.random() > 0.5:
                    content.insert(pos, ord(' '))
                else:
                    content[pos] = ord('\t')
        elif mod_type == 2:  # Modify newline
            newlines = [i for i, byte in enumerate(content) if byte == ord('\n')]
            if newlines:
                pos = random.choice(newlines)
                if random.random() > 0.5:
                    content.insert(pos, ord('\n'))
                else:
                    content.insert(pos+1, ord(' '))
    
    os.makedirs("variants", exist_ok=True)
    variant_path = f"variants/{os.path.basename(original_file).split('.')[0]}_variant_{variant_num}.txt"
    with open(variant_path, "wb") as f:
        f.write(content)
    return variant_path

def find_collision(doc1, doc2, max_variants=5000):
    print(f"Starting birthday attack to find collision (first 16 bits of MD5)...")
    print(f"Document 1: {doc1}")
    print(f"Document 2: {doc2}")
    
    doc1_hashes = {}
    doc2_hashes = {}
    
    for i in range(max_variants):
        if i % 1000 == 0:
            print(f"Testing variant {i}...")
        
        # Process doc1
        variant1 = create_variant(doc1, i)
        hash1, _ = get_md5(variant1)
        truncated1 = hash1[:4]  # First 16 bits 
        
        if truncated1 in doc2_hashes:
            print(f"\nCollision found! Variant {i}")
            print(f"First 16 bits of MD5 hash: {truncated1}")
            print(f"Favorable variant: {variant1}")
            print(f"Unfavorable variant: {doc2_hashes[truncated1]}")
            
            # Save the colliding files for easy access
            with open("collision_favorable.txt", "wb") as f:
                with open(variant1, "rb") as src:
                    f.write(src.read())
            with open("collision_unfavorable.txt", "wb") as f:
                with open(doc2_hashes[truncated1], "rb") as src:
                    f.write(src.read())
                    
            return variant1, doc2_hashes[truncated1], truncated1
        
        doc1_hashes[truncated1] = variant1
        
        # Process doc2
        variant2 = create_variant(doc2, i)
        hash2, _ = get_md5(variant2)
        truncated2 = hash2[:4]  # First 16 bits (4 hex chars)
        
        if truncated2 in doc1_hashes:
            print(f"\nCollision found! Variant {i}")
            print(f"First 16 bits of MD5 hash: {truncated2}")
            print(f"Favorable variant: {doc1_hashes[truncated2]}")
            print(f"Unfavorable variant: {variant2}")
            
            # Save the colliding files for easy access
            with open("collision_favorable.txt", "wb") as f:
                with open(doc1_hashes[truncated2], "rb") as src:
                    f.write(src.read())
            with open("collision_unfavorable.txt", "wb") as f:
                with open(variant2, "rb") as src:
                    f.write(src.read())
                    
            return doc1_hashes[truncated2], variant2, truncated2
        
        doc2_hashes[truncated2] = variant2
    
    print(f"\nNo collision found after testing {max_variants} variants.")
    return None, None, None

if __name__ == "__main__":
    doc1 = "contract_favorable.txt"
    doc2 = "contract_unfavorable.txt"
    
    if not os.path.exists(doc1) or not os.path.exists(doc2):
        print("Please create the two contract files first!")
        exit()
    
    find_collision(doc1, doc2)
