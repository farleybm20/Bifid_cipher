def create_polybius_square(key):
    # Normalize the key: convert to uppercase, replace 'J' with 'I', and remove duplicates
    key = key.upper().replace('J', 'I')  # Replace 'J' with 'I'
    key = ''.join(sorted(set(key), key=key.index))  # Remove duplicates, preserve order
    
    # Define the Polybius alphabet (without 'J')
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for char in key:
        if char not in alphabet:
            raise ValueError(f"Invalid character '{char}' in key.")
    
    # Construct the Polybius square
    square = key  # Start with the key
    for char in alphabet:
        if char not in key:
            square += char  # Add remaining letters of the alphabet
    
    return [square[i:i+5] for i in range(0, 25, 5)]


def find_coordinates(square, char):
    for row_index, row in enumerate(square):
        if char in row:
            return row_index, row.index(char)
    return None

def bifid_encrypt(plaintext, key, period):
    # Step 1: Create the Polybius square
    square = create_polybius_square(key)
    plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')
    
    # Step 2: Convert plaintext to coordinates (rows and columns)
    rows, cols = [], []
    for char in plaintext:
        row, col = find_coordinates(square, char)
        rows.append(row + 1)  # Add 1 to match the example (1-based indexing)
        cols.append(col + 1)
    
    # Combine rows and columns
    combined = rows + cols
    
    # Step 3: Group by the period
    grouped = []
    for i in range(0, len(combined), period * 2):
        grouped.extend(combined[i:i+period] + combined[i+period:i+period*2])
    
    # Step 4: Convert back to text using the Polybius square
    ciphertext = ''
    for i in range(0, len(grouped), 2):
        row, col = grouped[i] - 1, grouped[i + 1] - 1  # Convert back to 0-based indexing
        ciphertext += square[row][col]
    
    return ciphertext


def bifid_decrypt(ciphertext, key, period):
    square = create_polybius_square(key)
    ciphertext = ciphertext.upper().replace(' ', '')
    
    combined = []
    for char in ciphertext:
        row, col = find_coordinates(square, char)
        combined.append(row)
        combined.append(col)
    
    half = len(combined) // 2
    rows, cols = combined[:half], combined[half:]
    plaintext = ''
    for row, col in zip(rows, cols):
        plaintext += square[row][col]
    return plaintext

# Example usage
# if __name__ == "__main__":
#     mode = input("Enter mode (encrypt/decrypt): ").strip().lower()
#     message = input("Enter the message: ").strip()
#     key = input("Enter the key: ").strip()
#     period = int(input("Enter the period: ").strip())
    
#     if mode == 'encrypt':
#         print("Encrypted message:", bifid_encrypt(message, key, period))
#     elif mode == 'decrypt':
#         print("Decrypted message:", bifid_decrypt(message, key, period))
#     else:
#         print("Invalid mode. Please choose 'encrypt' or 'decrypt'.")

print('Encrypted message: ', bifid_encrypt('defend the east wall of the castle', 'phqgmeaylnofdxkrcvszwbuti',5))
