import os
import shutil
import configparser
import getpass
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from tqdm import tqdm

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def should_copy(file_path):
    for skip in ['__pycache__', '.git']:
        if skip in file_path:
            return False
    return True

def copy_project_files(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        # Skip unwanted dirs
        dirs[:] = [d for d in dirs if should_copy(os.path.join(root, d))]
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dst, rel_path)
        os.makedirs(dest_path, exist_ok=True)
        for file in files:
            if should_copy(file):
                shutil.copy2(os.path.join(root, file), os.path.join(dest_path, file))
    print(f"✅ Project copied to {dst}")

def scp_transfer_with_progress(dst_dir, remote_info):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    username = remote_info['username']
    hostname = remote_info['client_ip']
    remote_path = remote_info['remote_path']

    while True:
        try:
            password = getpass.getpass(prompt=f"🔐 Enter password for {username}@{hostname}: ")
            client.connect(hostname, username=username, password=password)

            def progress(filename, size, sent):
                percent = sent / size * 100
                print(f"\r📦 Uploading {os.path.basename(filename)}: {percent:.2f}%", end='')

            with SCPClient(client.get_transport(), progress=progress) as scp:
                print(f"\n📤 Starting transfer to {username}@{hostname}:{remote_path}")
                scp.put(dst_dir, recursive=True, remote_path=remote_path)
                print("\n✅ Transfer completed successfully.")
            break
        except Exception as e:
            print(f"❌ Transfer failed: {e}")
            retry = input("🔁 Try again? (y/n): ").strip().lower()
            if retry != 'y':
                break

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
