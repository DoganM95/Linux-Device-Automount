docker build -t doganm95/linux-device-automount .
docker run `
    -d `
    -e POLLING_INTERVAL=5 `
    -v /dev:/dev `
    -v /some/host/mount/folder:/usb `
    --name doganm95-linux-device-automount `
    doganm95/linux-device-automount