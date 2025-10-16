## Intro

Automatically mount (mass storage) devices attached via usb to a linux host as sub-folders inside a user-defined parent folder.

## Features

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

## Docker

```bash
docker run \
    -d \
    --privileged \
    -e POLLING_INTERVAL=5 \
    -v /dev:/dev \
    -v /parent_folder:/usb:rshared \
    --name doganm95-linux-device-automount \
    ghcr.io/doganm95/linux-device-automount:latest
```

- Replace `/parent_folder` with the parent folder, you want the mass storage devices mounted in as sub-folders
- Replace `POLLING_INTERVAL` with the time in seconds the detection loop should wait between each iteration
- Don't touch `/dev:/dev`, this is necessary to let the container access the host devices
