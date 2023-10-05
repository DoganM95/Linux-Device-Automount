docker build -t automount .
docker run `
    -e SLEEP_DURATION=5 `
    -e MOUNT_PARENT_DIR=/mnt `
    -v /dev:/dev `
    -v /some/host/mount/folder:/mnt `
    --name device-automount `
    automount