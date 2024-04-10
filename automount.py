import os
import time
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)

POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', 5))
MOUNT_PARENT_DIR = '/usb'

active_mounts = set()
allowed_filesystems = {'ntfs', 'exfat', 'xfs', 'vfat', 'ext4', 'ext3', 'ext2', 'fat32', 'fat16'}

def unmount_existing_devices():
    global active_mounts
    for mount_point in os.listdir(MOUNT_PARENT_DIR):
        full_mount_point = os.path.join(MOUNT_PARENT_DIR, mount_point)
        if os.path.isdir(full_mount_point):
            try:
                subprocess.run(['umount', '-l', full_mount_point], check=True)
                logging.info(f"Unmounted existing device at {full_mount_point}")
            except Exception as e:
                logging.error(f"Failed to unmount existing device at {full_mount_point}: {e}")
    active_mounts = set()

def remove_empty_dirs(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            full_dirpath = os.path.join(dirpath, dirname)
            try:
                if not os.listdir(full_dirpath):
                    logging.info(f"Removing empty directory: {full_dirpath}")
                    os.rmdir(full_dirpath)
            except Exception as e:
                logging.warning(f"Could not remove directory {full_dirpath}: {e}")

def get_device_info():
    try:
        output = subprocess.check_output(['lsblk', '--json'])
        return json.loads(output)
    except Exception as e:
        logging.error(f"Failed to run lsblk: {e}")
        return None

def get_filesystem(device):
    try:
        output = subprocess.check_output(['blkid', '-o', 'export', device])
        lines = output.decode('utf-8').strip().split('\n')
        for line in lines:
            if line.startswith('TYPE='):
                return line.split('TYPE=')[1]
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to fetch filesystem type for {device}: {e}")
        return None

def mount_device(device, mount_point, fs_type):
    try:
        subprocess.run(['mount', '-t', fs_type, device, mount_point], check=True)
        logging.info(f"Device {device} mounted at {mount_point} with filesystem {fs_type}")
    except Exception as e:
        logging.error(f"Failed to mount {device}: {e}")

if __name__ == '__main__':
    logging.info("Starting device monitoring")
    
    unmount_existing_devices()

    prev_devs = set()
    while True:
        remove_empty_dirs(MOUNT_PARENT_DIR)
        
        current_devs = set([dev for dev in os.listdir('/dev') if 'sd' in dev])
        added_devs = current_devs - prev_devs
        removed_devs = prev_devs - current_devs

        for dev in added_devs:
            logging.info(f"New device detected: {dev}")
            dev_path = f"/dev/{dev}"
            fs_type = get_filesystem(dev_path)
            if fs_type and fs_type.lower() in allowed_filesystems:
                mount_point = f"{MOUNT_PARENT_DIR}/{dev}"
                if not os.path.exists(mount_point):
                    os.makedirs(mount_point)
                mount_device(dev_path, mount_point, fs_type)

        for dev in removed_devs:
            logging.info(f"Device removed: {dev}")
            mount_point = f"{MOUNT_PARENT_DIR}/{dev}"
            try:
                subprocess.run(['umount', '-l', mount_point], check=True)
                logging.info(f"Device at {mount_point} has been unmounted")
            except Exception as e:
                logging.error(f"Failed to unmount {mount_point}: {e}")

        prev_devs = current_devs
        time.sleep(POLLING_INTERVAL)
