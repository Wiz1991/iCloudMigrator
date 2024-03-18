import os
import sys
from pyicloud import PyiCloudService
from tqdm import tqdm
import shutil

email = input('Enter your email')
password = input('Enter your password')

api = PyiCloudService(email, password)

if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")


target = input("Enter path of target folder to upload")
icloud_target = input("Enter iCloud Drive folder to upload at")

for root, dirs, files in os.walk(target):
    for file in tqdm(files):
        file_path = os.path.join(root, file)

        shutil.copy(src=file_path, dst='.')
    
        with open(file, "rb") as f:
            api.drive[icloud_target].upload(f)
    
        os.remove(file)