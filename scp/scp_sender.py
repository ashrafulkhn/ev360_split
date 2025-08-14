
# ********************************************
#  *********** INSTALLATION GUIDE ***********
# ********************************************
# 
# Dependencies:
# Python: python3
# Packages: pip install paramiko scp tqdm
# Uncomment these lines in the remote device for sshd_config
# vi /etc/ssh/sshd_config
# 
# PermitRootLogin yes
# PasswordAuthentication yes
# UsePAM no
# 
# sudo systemctl restart sshd
# 
# To set new password if not present or remove passwords
# ssh-keygen


import os
import shutil
import configparser
import getpass
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from paramiko.ssh_exception import AuthenticationException, SSHException

CONFIG_FILE = 'config.ini'

def should_copy(file_path):
    name = os.path.basename(file_path)
    if name.startswith('.') or name == '__pycache__':
        return False
    return True

def create_config():
    config = configparser.ConfigParser()

    print("🛠 Creating new config.ini file:")
    config['project'] = {
        'source_dir': input("Enter source directory path: ").strip(),
        'destination_dir': input("Enter temporary destination directory path: ").strip()
    }
    config['remote'] = {
        'username': input("Enter remote username: ").strip(),
        'client_ip': input("Enter remote IP address: ").strip(),
        'remote_path': input("Enter remote destination path: ").strip()
    }

    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    print("✅ Config file created.\n")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        create_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def clean_directory(dst):
    print(f"🧹 Cleaning contents of {dst}...")
    for root, dirs, files in os.walk(dst, topdown=False):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                print(f"⚠️ Failed to delete file: {file} -> {e}")
        for dir in dirs:
            try:
                shutil.rmtree(os.path.join(root, dir))
            except Exception as e:
                print(f"⚠️ Failed to delete directory: {dir} -> {e}")
    print("✅ Cleaned destination directory.\n")

def copy_project_files(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"📂 Created destination directory: {dst}")
    else:
        if any(os.scandir(dst)):
            clean_directory(dst)
        else:
            print(f"📁 Destination directory {dst} is already empty.\n")

    print(f"📁 Copying project files from {src} to {dst}...\n")

    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if should_copy(os.path.join(root, d))]
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dst, rel_path)
        os.makedirs(dest_path, exist_ok=True)

        for file in files:
            full_file_path = os.path.join(root, file)
            if should_copy(full_file_path):
                shutil.copy2(full_file_path, os.path.join(dest_path, file))

    print("✅ Project files copied successfully.\n")

def scp_transfer_with_progress(dst_dir, remote_info):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    username = remote_info['username']
    hostname = remote_info['client_ip']
    remote_path = remote_info['remote_path']

    print(f"🌐 Connecting to {username}@{hostname}...")

    # Try without password (key-based or empty password)
    tried_password = False
    password = None

    while True:
        try:
            client.connect(
                hostname,
                username=username,
                password=password if tried_password else None,
                timeout=10,
                allow_agent=True,
                look_for_keys=True
            )
            break  # connected successfully
        except AuthenticationException:
            if tried_password:
                print("🔒 Authentication failed.")
            password = getpass.getpass(prompt=f"🔐 Enter password for {username}@{hostname} (leave empty for no password): ")
            tried_password = True
        except SSHException as e:
            print(f"⚠️ SSH Error: {e}")
            retry = input("🔁 Retry connection? (y/n): ").strip().lower()
            if retry != 'y':
                return
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return

    def progress(filename, size, sent):
        percent = sent / size * 100 if size else 100
        print(f"\r📦 Uploading {os.path.basename(filename)}: {percent:.2f}%", end='')

    try:
        with SCPClient(client.get_transport(), progress=progress) as scp:
            print(f"\n📤 Starting transfer to {username}@{hostname}:{remote_path}")
            scp.put(dst_dir, recursive=True, remote_path=remote_path)
            print("\n✅ Transfer completed successfully.")
    except Exception as e:
        print(f"\n❌ SCP transfer failed: {e}")
    finally:
        client.close()

def main():
    config = load_config()

    source_dir = config['project']['source_dir']
    destination_dir = config['project']['destination_dir']
    remote_info = {
        'username': config['remote']['username'],
        'client_ip': config['remote']['client_ip'],
        'remote_path': config['remote']['remote_path']
    }

    copy_project_files(source_dir, destination_dir)
    scp_transfer_with_progress(destination_dir, remote_info)

if __name__ == "__main__":
    main()
