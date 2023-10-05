import subprocess
import json
import pyudev

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
                return line.split('=')[1]
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
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            dev_path = device.device_node
            if 'usb' in dev_path:
                device_info = get_device_info()
                for block_device in device_info.get('blockdevices', []):
                    if block_device.get('name') in dev_path:
                        mount_point = f"/media/{block_device['name']}"
                        fs_type = get_filesystem(dev_path)
                        if fs_type:
                            mount_device(dev_path, mount_point, fs_type)

        elif device.action == 'remove':
            dev_path = device.device_node
            if 'usb' in dev_path:
                mount_point = f"/media/{dev_path.split('/')[-1]}"
                unmount_device(mount_point)
