from PIL import Image

# Function to read file contents
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Function to write content to a file
def write_to_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

# File paths
text_file_path = "file_to_embed.txt"
input_image_path = "original_image.jpg"
output_image_path = "output_image.jpg"
extracted_text_file_path = "extracted_text.txt"

# Read text file content
file_content = read_file_content(text_file_path)

# Embedding
def embed_message(image_path, message):
    img = Image.open(image_path).convert('L')  # Convert image to grayscale
    pixels = img.load()
    message += "\0" * (len(message) % 3)  # Pad message to be divisible by 3
    message_bytes = [ord(char) for char in message]
    message_idx = 0
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if message_idx < len(message_bytes):
                pixel_value = pixels[x, y]
                new_pixel_value = pixel_value + (message_bytes[message_idx] & 3)
                pixels[x, y] = new_pixel_value
                message_idx += 1
    img.save(output_image_path)

embed_message(input_image_path, file_content)
print("Text file embedded successfully.")

# Extraction
def extract_message(image_path):
    img = Image.open(image_path).convert('L')  # Convert image to grayscale
    pixels = img.load()
    message_bytes = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel_value = pixels[x, y]
            message_bytes.append(pixel_value & 3)
    return ''.join([chr(byte) for byte in message_bytes]).rstrip('\0')

extracted_content = extract_message(output_image_path)
print("Extracted content from image:")
print(extracted_content)

# Write extracted content to a text file
write_to_file(extracted_content, extracted_text_file_path)
print("Extracted content written to:", extracted_text_file_path)
