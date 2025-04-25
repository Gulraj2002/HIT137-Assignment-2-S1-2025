#!/usr/bin/env python
# coding: utf-8

# In[3]:


def scramble_text(plain_text, key_n, key_m):
    """
    Transforms the input text into an encoded format based on two secret keys.

    This function applies different shifting rules to lowercase and uppercase
    letters depending on their position in the alphabet, while numbers and
    special characters remain as they are.

    Args:
        plain_text (str): The original text to be encoded.
        key_n (int): The first secret integer key influencing the encoding.
        key_m (int): The second secret integer key affecting the encoding process.

    Returns:
        str: The encoded text.
    """
    cipher_text = ""
    for symbol in plain_text:
        if 'a' <= symbol <= 'z':
            if symbol <= 'm':
                # Shift forward for first half of lowercase letters
                shifted_val = (ord(symbol) - ord('a') + key_n * key_m) % 26
                cipher_text += chr(shifted_val + ord('a'))
            else:
                # Shift backward for second half of lowercase letters
                shifted_val = (ord(symbol) - ord('a') - (key_n + key_m)) % 26
                cipher_text += chr(shifted_val + ord('a'))
        elif 'A' <= symbol <= 'Z':
            if symbol <= 'M':
                # Shift backward for first half of uppercase letters
                shifted_val = (ord(symbol) - ord('A') - key_n) % 26
                cipher_text += chr(shifted_val + ord('A'))
            else:
                # Shift forward for second half of uppercase letters
                shifted_val = (ord(symbol) - ord('A') + key_m**2) % 26
                cipher_text += chr(shifted_val + ord('A'))
        else:
            # Keep non-alphabetic characters unchanged
            cipher_text += symbol
    return cipher_text

def un_scramble_text(encoded_text, key_n, key_m):
    """
    Reverses the encoding process to retrieve the original text.

    This function applies the inverse shifting rules based on the same secret
    keys used for encoding.

    Args:
        encoded_text (str): The encoded text to be decoded.
        key_n (int): The first secret integer key used for decoding.
        key_m (int): The second secret integer key used for decoding.

    Returns:
        str: The original, decoded text.
    """
    original_text = ""
    for symbol in encoded_text:
        if 'a' <= symbol <= 'z':
            if symbol <= 'm':
                # Reverse shift for first half of lowercase letters
                shifted_val = (ord(symbol) - ord('a') - key_n * key_m) % 26
                original_text += chr(shifted_val + ord('a'))
            else:
                # Reverse shift for second half of lowercase letters
                shifted_val = (ord(symbol) - ord('a') + (key_n + key_m)) % 26
                original_text += chr(shifted_val + ord('a'))
        elif 'A' <= symbol <= 'Z':
            if symbol <= 'M':
                # Reverse shift for first half of uppercase letters
                shifted_val = (ord(symbol) - ord('A') + key_n) % 26
                original_text += chr(shifted_val + ord('A'))
            else:
                # Reverse shift for second half of uppercase letters
                shifted_val = (ord(symbol) - ord('A') - key_m**2) % 26
                original_text += chr(shifted_val + ord('A'))
        else:
            # Keep non-alphabetic characters unchanged
            original_text += symbol
    return original_text

def verify_integrity(original, recovered):
    """
    Compares the recovered text with the original to ensure they are identical.

    Args:
        original (str): The initial text.
        recovered (str): The text obtained after decoding.

    Returns:
        bool: True if the texts are an exact match, False otherwise.
    """
    return original == recovered

def text_handling_process():
    """
    Orchestrates the reading of a file, encoding its content, saving the
    encoded text, decoding it, and verifying the process.
    """
    input_filename = "raw_text.txt"
    output_filename = "encrypted_text.txt"

    try:
        with open(input_filename, "r") as source_file:
            plain_content = source_file.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        return

    first_key = int(input("Enter the first encoding key (an integer): "))
    second_key = int(input("Enter the second encoding key (an integer): "))

    encoded_content = scramble_text(plain_content, first_key, second_key)

    try:
        with open(output_filename, "w") as destination_file:
            destination_file.write(encoded_content)
        print(f"Encoding complete. Encoded text saved to '{output_filename}'.")
    except Exception as e:
        print(f"Error writing to '{output_filename}': {e}")
        return

    decoded_content = un_scramble_text(encoded_content, first_key, second_key)

    if verify_integrity(plain_content, decoded_content):
        print("Decoding successful! The recovered text matches the original.")
    else:
        print("Decoding verification failed. The recovered text is different from the original.")

if __name__ == "__main__":
    text_handling_process()


# In[ ]:




