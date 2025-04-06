import os
from gofilepy import GofileClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
import humanize
client = GofileClient()

def encode_file(name: str) -> MultipartEncoder:
    try:
        mp_encoder = MultipartEncoder(
            fields={
                'filesUploaded': (name, open(name, 'rb'))
            }
        )
        return mp_encoder
    except Exception as e:
        print(f"Error encoding file {name}: {e}")
        return None
def upload_to_gofile(filepath):
    file = client.upload(file=open(filepath, "rb"))
    return {
        "fileName": file.name,
        "downloadPage": file.page_link,
        "fileHash": file.md5,
        "fileSize": file.size
    }
def upload_directory_to_gofile(directory_path, output_file="links.txt"):
    if not os.path.isdir(directory_path):
        raise ValueError(f"{directory_path} is not a valid directory.")
    uploaded_files = []
    with open(output_file, 'w') as link_file:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    print(f"Uploading file: {file_path}")
                    metadata = upload_to_gofile(file_path)
                    uploaded_files.append(metadata)
                    link_file.write(f"💠==============================💠\n")
                    link_file.write(f"💠  File Directory: {file_path}💠\n")
                    link_file.write(f"💠  Download Page: {metadata['downloadPage']}💠\n")
                    link_file.write(f"💠  File Hash: {metadata['fileHash']}💠\n")
                    link_file.write(f"💠  Size: {humanize.naturalsize(metadata['fileSize'])}💠\n")
                    link_file.write(f"💠==============================💠\n")
                except Exception as e:
                    print(f"Failed to upload {file_path}: {e}")
    return uploaded_files
