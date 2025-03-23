import os
import requests

def upload_to_gofile(file_path):
    server = "store1"
    upload_url = f"https://{server}.gofile.io/uploadFile"

    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'file': file})
    
    if response.status_code != 200:
        raise Exception("File upload failed.")

    data = response.json()
    if data["status"] != "ok":
        raise Exception(f"Error uploading file: {data.get('message', 'Unknown error')}")

    file_info = data.get("data", {})
    required_keys = ["name", "downloadPage", "md5", "size"]
    for key in required_keys:
        if key not in file_info:
            raise KeyError(f"Missing key '{key}' in response: {file_info}")

    return {
        "fileName": file_info["name"],
        "downloadPage": file_info["downloadPage"],
        "fileHash": file_info["md5"],
        "fileSize": file_info["size"]
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
                    metadata = upload_to_gofile(file_path)
                    uploaded_files.append(metadata)

                    link_file.write(f"==============================\n")
                    link_file.write(f"{file_path}:\n")
                    link_file.write(f"  Download Page: {metadata['downloadPage']}\n")
                    link_file.write(f"  File Hash: {metadata['fileHash']}\n")
                    link_file.write(f"  Size: {metadata['fileSize']} bytes\n")
                    link_file.write(f"==============================\n")

                except Exception as e:
                    print(f"Failed to upload {file_path}: {e}")

    return uploaded_files
