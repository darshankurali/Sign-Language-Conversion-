import os

def generate_labels_from_gifs(folder_path):
    """
    Generate a list of labels from GIF filenames in a folder.

    Args:
        folder_path (str): Path to the folder containing GIF files.

    Returns:
        list: A list of labels (filenames without extensions).
    """
    labels = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".gif"):  # Only include .gif files
            label = os.path.splitext(filename)[0]  # Remove the file extension
            labels.append(label)
    return labels

# Example Usage
gif_folder = "ISL_Gifs"  # Replace with the path to your GIF folder

#def create_labels():
isl_gif = generate_labels_from_gifs(gif_folder)
print(isl_gif)
print("Number of elements:", len(isl_gif))

