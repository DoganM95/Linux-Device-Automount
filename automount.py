import os
import time
import subprocess
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', 5))
MOUNT_PARENT_DIR = '/usb'

# Currently activemount points
active_mounts = set()

# List of allowed filesystems
allowed_filesystems = {'ntfs', 'exfat', 'xfs', 'vfat', 'ext4', 'ext3', 'ext2', 'fat32', 'fat16'}

def remove_empty_dirs(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            full_dirpath = os.path.join(dirpath, dirname)
            if not os.listdir(full_dirpath) and full_dirpath not in active_mounts:
                logging.info(f"Removing empty directory: {full_dirpath}")
                os.rmdir(full_dirpath)

def get_device_info():
    try:
        output = subprocess.check_output(['lsblk', '--json'])
        return json.loads(output)
    except Exception as e:
        logging.error(f"Failed to run lsblk: {e}")
        return None

def get_filesystem(device):
    try:
        command = ['blkid', '-o', 'export', device]
        logging.info(f"Running command: {' '.join(command)}")
        output = subprocess.check_output(command)
        lines = output.decode('utf-8').strip().split('\n')
        for line in lines:
            if line.startswith('TYPE='):
                return line.split('TYPE=')[1]
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to fetch filesystem type for {device}: {e}")
        return None

def mount_device(device, mount_point, fs_type):
    if fs_type and fs_type.lower() in allowed_filesystems:
        try:
            subprocess.run(['mount', '-t', fs_type, device, mount_point], check=True)
            logging.info(f"Device {device} mounted at {mount_point} with filesystem {fs_type}")
            active_mounts.add(mount_point)  # Add to active mounts
        except Exception as e:
            logging.error(f"Failed to mount {device}: {e}")

def unmount_device(mount_point, fs_type):
    if fs_type and fs_type.lower() in allowed_filesystems:
        try:
            subprocess.run(['umount', mount_point], check=True)
            logging.info(f"Device at {mount_point} has been unmounted")
            if mount_point in active_mounts:
                active_mounts.remove(mount_point)  # Remove from active mounts
        except Exception as e:
            logging.error(f"Failed to unmount {mount_point}: {e}")
    else:
        logging.error(f"Filesystem type is None. Cannot proceed with unmount.")

if __name__ == '__main__':
    logging.info("Starting device monitoring")
    prev_devs = set()
    while True:
        remove_empty_dirs(MOUNT_PARENT_DIR)
        
        current_devs = set(os.listdir('/dev'))
        added_devs = current_devs - prev_devs
        removed_devs = prev_devs - current_devs

        for dev in added_devs:
            if 'sd' in dev:
                logging.info(f"New device detected: {dev}")
                dev_path = f"/dev/{dev}"
                fs_type = get_filesystem(dev_path)
                if fs_type:
                    mount_point = f"{MOUNT_PARENT_DIR}/{dev}"
                    if not os.path.exists(mount_point):
                        os.makedirs(mount_point)
                    mount_device(dev_path, mount_point, fs_type)

        for dev in removed_devs:
            if 'sd' in dev:
                logging.info(f"Device removed: {dev}")
                mount_point = f"{MOUNT_PARENT_DIR}/{dev}"
                unmount_device(mount_point)

        prev_devs = current_devs
        time.sleep(POLLING_INTERVAL)
