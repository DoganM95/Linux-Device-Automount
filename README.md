## Intro
Docker container to automatically mount linux devices (mass storage devices attached via usb) to subfolders in a specified parent folder, bound as a volume.
Intended for use on a DIY NAS running Rockstor, which is missing this capability but probably works universally.

## Functionality
- Initially unmounts all devices that had a subdir in the volume that is bound to /usb
- Automatically mounts devices with filesystem of type `{'ntfs', 'exfat', 'xfs', 'vfat', 'ext4', 'ext3', 'ext2', 'fat32', 'fat16'}`
- Mounted folder becomes a subdirectory of the parent (see volume) named after its partition-name

## Example
If the container runs with e.g. `-v "/mnt/external/devices:/usb:rshared"`, the devices connected to the host via usb would mount under `mnt/external/devices`.
E.g. a usb stick with 4 GB with a partition formatted to exFat would ususally pop up as `/dev/sdX`, in this example `/dev/sdb`. The device tree of `lsblk` would look like this:
```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sdb           8:64   0 931.5G  0 disk
└─sdb1        8:65   0    16M  0 part
```
The container would recognize the new `sdX` device (here `sdb`) and mount its partition(s) under `/mnt/external/devices/sdb1` and so on, if more than one partition exists, resulting in
```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sde           8:64   0 931.5G  0 disk
└─sdb1        8:66   0 931.5G  0 part /mnt/external/devices/sdb1
```
The partition is now mounted as a folder and can be accessed using shell, UI, FTP, SMB, whatever.

## Setup
https://hub.docker.com/r/doganm95/linux-device-automount
