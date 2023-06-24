import os
import cv2

def batch_resize_images(input_dir, output_dir, target_size):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the list of image file names in the input directory
    file_names = os.listdir(input_dir)

    for file_name in file_names:
        # Construct the input and output file paths
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        # Load the image
        image = cv2.imread(input_path)

        # Resize the image to the target size
        resized_image = cv2.resize(image, target_size)

        # Save the resized image
        cv2.imwrite(output_path, resized_image)

# Usage example
input_directory = 'C:/gb_ksh/python/loverdog/loverdog/_media/dog_images/test'
output_directory = 'C:/gb_ksh/python/loverdog/loverdog/_media/dog_images/processed_image'
target_size = (224, 224)

batch_resize_images(input_directory, output_directory, target_size)
