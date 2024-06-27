import os
import matplotlib.pyplot as plt
from datetime import datetime

def count_files(directory, image_extensions=None, video_extensions=None):
    """
    Count image and video files in the given directory (non-recursive).
    
    Parameters:
    - directory (str): Path to the directory.
    - image_extensions (tuple): Extensions considered as image files.
    - video_extensions (tuple): Extensions considered as video files.
    
    Returns:
    - tuple: (image_count, video_count)
    """
    if image_extensions is None:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    if video_extensions is None:
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv')

    image_count = 0
    video_count = 0

    try:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                if file.lower().endswith(image_extensions):
                    image_count += 1
                elif file.lower().endswith(video_extensions):
                    video_count += 1
    except Exception as e:
        print(f"Error counting files in {directory}: {e}")
        raise

    return image_count, video_count

def create_graph(image_count, video_count, output_path):
    """
    Create and save a bar graph of image and video counts.
    
    Parameters:
    - image_count (int): Number of image files.
    - video_count (int): Number of video files.
    - output_path (str): Path to save the graphic.
    """
    categories = ['Images', 'Videos']
    counts = [image_count, video_count]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts, color=['blue', 'red'])
    plt.xlabel('File Type')
    plt.ylabel('Count')
    plt.title('Number of Images and Videos')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

def ensure_directory_exists(directory):
    """
    Ensure that the specified directory exists.
    
    Parameters:
    - directory (str): Path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_directory_path():
    """
    Prompt the user to enter a valid directory path.
    
    Returns:
    - str: Validated directory path.
    """
    while True:
        directory = input("Enter the path to the directory: ")
        if os.path.isdir(directory):
            return directory
        else:
            print(f"The path '{directory}' is not a valid directory. Please try again.")

def get_output_filename():
    """
    Prompt the user to enter a filename and append the current date.
    
    Returns:
    - str: Filename with the current date appended.
    """
    filename = input("Enter the base name for the output file: ")
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f"{filename}_{current_date}.png"

def main():
    # Get the directory path from the user
    directory = get_directory_path()
    output_directory = os.path.join(directory, 'results')
    
    # Ensure the results directory exists
    ensure_directory_exists(output_directory)
    
    try:
        # Count image and video files in the directory
        image_count, video_count = count_files(directory)
        
        # Get the output filename from the user and append the current date
        output_filename = get_output_filename()
        output_path = os.path.join(output_directory, output_filename)
        
        # Create and save the graphic
        create_graph(image_count, video_count, output_path)
        
        print(f'Results saved in {output_path}')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()