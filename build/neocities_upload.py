
import os
from neocities import NeoCities
from neocities_key import key
import generatePages

def main():


    client = NeoCities(user="mhoff", key=key)
    
    ignored_filenames = [
        ".gitignore"
    ]

    file_uploads = []
    
    html_dir = "../public_html"
    for (directory, directories, files) in os.walk(html_dir):
        for file_name in files:
            if file_name in ignored_filenames:
                continue

            file_to_upload_path = os.path.normpath(os.path.join(directory, file_name)).replace("\\","/")
            neocities_path = os.path.relpath(file_to_upload_path, html_dir).replace("\\", "/")
            file_uploads.append((neocities_path, file_to_upload_path))
    
    print(f"Uploads:\n{file_uploads}")

    client.upload(*file_uploads)


if __name__ == "__main__":
    generatePages.main()

    main()