import os
import time

while True:
    drives = [d for d in os.listdir("/dev") if d.startswith("sd")]
    for drive in drives:
        partitions = [p for p in os.listdir(f"/dev/{drive}") if p.startswith(drive)]
        for part in partitions:
            mount_point = f"/mnt/{part}"
            if not os.path.exists(mount_point):
                os.makedirs(mount_point)
                os.system(f"mount /dev/{part} {mount_point}")
    time.sleep(10)
