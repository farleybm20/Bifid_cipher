import string

def clean_text(text):
    return ''.join(char.upper() for char in text if char.isalpha())

def create_polybius_square(key):
    key = key.upper().replace('J', 'I')  
    key = ''.join(sorted(set(key), key=key.index))  
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for char in key:
        if char not in alphabet:
            raise ValueError(f"Invalid character '{char}' in key.")
    
    square = key  
    for char in alphabet:
        if char not in key:
            square += char  
    
    return [square[i:i+5] for i in range(0, 25, 5)]


def find_coordinates(square, char):
    for row_index, row in enumerate(square):
        if char in row:
            return row_index, row.index(char)
    return None

def bifid_encrypt(plaintext, key, period):
    plaintext = clean_text(plaintext)
    square = create_polybius_square(key)
    plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')

    rows, cols = [], []
    for char in plaintext:
        row, col = find_coordinates(square, char)
        rows.append(row + 1)  
        cols.append(col + 1)

    combined = []
    for i in range(0, len(rows), period):
        combined.extend(rows[i:i + period] + cols[i:i + period])

    ciphertext = ''
    for i in range(0, len(combined), 2):
        row, col = combined[i] - 1, combined[i + 1] - 1  
        ciphertext += square[row][col]

    return ciphertext


def bifid_decrypt(ciphertext, key, period):
    square = create_polybius_square(key)
    ciphertext = ciphertext.upper().replace(' ', '')

    combined = []
    for char in ciphertext:
        row, col = find_coordinates(square, char)
        combined.append(row + 1)  
        combined.append(col + 1)

    rows, cols = [], []
    for i in range(0, len(combined), 2 * period):
        chunk = combined[i:i + 2 * period]
        split_point = len(chunk) // 2  
        rows.extend(chunk[:split_point])
        cols.extend(chunk[split_point:])

    plaintext = ''
    for row, col in zip(rows, cols):
        plaintext += square[row - 1][col - 1]  

    return plaintext



if __name__ == "__main__":
    mode = input("Enter mode (encrypt/decrypt): ").strip().lower()
    message = input("Enter the message: ").strip()
    key = input("Enter the key: ").strip()
    period = int(input("Enter the period: ").strip())
    
    if mode == 'encrypt':
        print("Encrypted message:", bifid_encrypt(message, key, period))
    elif mode == 'decrypt':
        print("Decrypted message:", bifid_decrypt(message, key, period))
    else:
        print("Invalid mode. Please choose 'encrypt' or 'decrypt'.")

