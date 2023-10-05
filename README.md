# Linux-Dev-Automount
Docker container to mount linux devices to a specified parent folder

# Tests
- `lsblk` to get currently attached disks and their sdX
- `mkdir ...` to create a directory to mount the device to
- `blkid /dev/sdXY` to get info like file system type with X being the disk char and Y being the partition number
- `mount -t exfat /dev/sdXY /destination` to mount an exfat partition 
