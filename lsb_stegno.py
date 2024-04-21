from stegano import lsb
# Function to read file contents
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Function to write content to a file
def write_to_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

# Function to embed the file in image

def embed(input_image,file,output_image="output_image.png"):
    #file_content = read_file_content(file)
    file_content=file
    lsb.hide(input_image, file_content).save(output_image)
    with open("output_image.png", "rb") as file:
        image_data = file.read()
    return image_data

# Function to extract file content from image

def extract(input_image):
    extracted_content = lsb.reveal(input_image)
    return extracted_content

