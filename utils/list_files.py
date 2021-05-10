import os


def list_of_files(folder_path):
    """
    A method that finds the names of all files within the specified folder location.
    :parameter folder_path - A string that represents the path to the folder.
    :returns List of file names in the specified folder
    """

    file_list = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in [f for f in filenames if f.endswith(".txt")]:
            file_list.append(str(os.path.join(dirpath, filename)))
    return file_list
