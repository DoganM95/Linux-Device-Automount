Docker container to automatically mount linux devices to subfolders in a specified parent folder bound as a volume.
Intended for use on a DIY NAS running Rockstor, which is missing this capability but probably works univarsally.

## Functionality
- Initially unmounts all devices that had a subdir in the volume that is bound to /usb
- Automatically mounts devices with filesystem of type `{'ntfs', 'exfat', 'xfs', 'vfat', 'ext4', 'ext3', 'ext2', 'fat32', 'fat16'}`
- Mounted folder becomes a subdirectory of the parent (see volume) named after its partition-name

## Setup
https://hub.docker.com/r/doganm95/linux-device-automount
