import subprocess
import time
import pyudev

def get_mount_point(device):
    try:
        output = subprocess.check_output(['udisksctl', 'mount', '--block-device', device])
        return output.decode('utf-8').split('at')[-1].strip()
    except subprocess.CalledProcessError:
        return None

def unmount_device(device):
    try:
        subprocess.run(['udisksctl', 'unmount', '--block-device', device])
    except subprocess.CalledProcessError:
        pass

if __name__ == '__main__':
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            dev_path = device.device_node
            if 'usb' in dev_path:
                mount_point = get_mount_point(dev_path)
                if mount_point:
                    print(f"Device {dev_path} mounted at {mount_point}")

        elif device.action == 'remove':
            dev_path = device.device_node
            if 'usb' in dev_path:
                unmount_device(dev_path)
                print(f"Device {dev_path} has been unmounted")
