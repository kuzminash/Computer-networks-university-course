from ftplib import FTP


def all_directories(ftp, all):
    all.append(ftp.pwd())
    for file_data in ftp.mlsd():
        file_name, meta = file_data
        file_type = meta.get('type')
        if file_type == 'dir':
            ftp.cwd(file_name)
            all_directories(ftp, all)
            ftp.cwd('..')

def upload_file(ftp):
    file_path = input()
    with open(file_path, "rb") as file:
        ftp.storbinary(f"STOR {file_path}", file)

def download_file(ftp):
    file_path = input()
    with open(file_path, "wb") as file:
        ftp.retrbinary(f"RETR {file_path}", file.write)

if __name__ == '__main__':
    serverName = input()
    ftp = FTP(serverName)
    USR = input()
    PASSWORD = input()
    ftp.connect()
    ftp.login(USR, PASSWORD)
    all_directories(ftp, [])
    upload_file(ftp)
    download_file(ftp)
    ftp.quit()

