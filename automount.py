import os
import time

mounted_points = set()

while True:
    try:
        # Get the list of all drives
        drives = [d for d in os.listdir("/dev") if d.startswith("sd")]
        new_mounts = set()

        for drive in drives:
            # List partitions on the drive
            partitions = [p for p in os.listdir(f"/dev/{drive}") if p.startswith(drive)]
            
            for part in partitions:
                mount_point = f"/mnt/{part}"

                # Check if already mounted
                if mount_point in mounted_points:
                    new_mounts.add(mount_point)
                    continue
                
                if not os.path.exists(mount_point):
                    os.makedirs(mount_point)

                # Attempt to mount the partition
                result = os.system(f"mount /dev/{part} {mount_point}")

                if result == 0:
                    print(f"Successfully mounted /dev/{part} to {mount_point}")
                    new_mounts.add(mount_point)
                else:
                    print(f"Failed to mount /dev/{part}")

        # Unmount any drives that were removed
        to_unmount = mounted_points - new_mounts
        for mount_point in to_unmount:
            print(f"Unmounting {mount_point}")
            os.system(f"umount {mount_point}")

        mounted_points = new_mounts

    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(10)
