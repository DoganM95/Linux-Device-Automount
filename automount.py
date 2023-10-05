import os
import time
import subprocess
import json
from dotenv import load_dotenv
from pathlib import Path

# Check if .env file exists
if Path('.env').is_file():
    load_dotenv()

# Load environment variables
POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', 5))  # Default value is 5
MOUNT_PARENT_DIR = os.getenv('MOUNT_PARENT_DIR', '/mnt')  # Default value is '/mnt'


def get_device_info():
    try:
        output = subprocess.check_output(['lsblk', '--json'])
        return json.loads(output)
    except subprocess.CalledProcessError:
        return None

def get_filesystem(device):
    try:
        output = subprocess.check_output(['blkid', '-o', 'export', device])
        lines = output.decode('utf-8').strip().split('\n')
        for line in lines:
            if line.startswith('TYPE='):
                return line.split('TYPE=')[1]
        return None
    except subprocess.CalledProcessError:
        return None

def mount_device(device, mount_point, fs_type):
    try:
        subprocess.run(['mount', '-t', fs_type, device, mount_point])
        print(f"Device {device} mounted at {mount_point} with file system {fs_type}")
    except subprocess.CalledProcessError:
        print(f"Failed to mount {device}")

def unmount_device(mount_point):
    try:
        subprocess.run(['umount', mount_point])
        print(f"Device at {mount_point} has been unmounted")
    except subprocess.CalledProcessError:
        print(f"Failed to unmount {mount_point}")

if __name__ == '__main__':
    prev_devs = set()
    while True:
        current_devs = set(os.listdir('/dev'))
        added_devs = current_devs - prev_devs
        removed_devs = prev_devs - current_devs

        for dev in added_devs:
            if 'sd' in dev:
                dev_path = f"/dev/{dev}"
                device_info = get_device_info()
                for block_device in device_info.get('blockdevices', []):
                    if block_device.get('name') in dev:
                        mount_point = f"{MOUNT_PARENT_DIR}/{block_device['name']}"
                        fs_type = get_filesystem(dev_path)
                        if fs_type:
                            mount_device(dev_path, mount_point, fs_type)

        for dev in removed_devs:
            if 'sd' in dev:
                mount_point = f"{MOUNT_PARENT_DIR}/{dev}"
                unmount_device(mount_point)

        prev_devs = current_devs
        time.sleep(POLLING_INTERVAL)
