docker build -t automount .
docker run `
    -e SLEEP_DURATION=5 `
    -v /dev:/dev `
    -v /some/host/mount/folder:/usb `
    --name device-automount `
    automount