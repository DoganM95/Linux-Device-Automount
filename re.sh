docker build -t doganm95/linux-device-automount .

# Production
docker run \
    --privileged \
    -e POLLING_INTERVAL=5 \
    -v /dev:/dev \
    -v /mnt2/homes/usb:/usb:rshared \
    --name doganm95-linux-device-automount \
    doganm95/linux-device-automount:latest

# Debug
# docker run \
#     --privileged \
#     -it \
#     --rm \
#     -e POLLING_INTERVAL=5 \
#     -v /dev:/dev \
#     -v /mnt2/homes/usb:/usb:rshared \
#     --name doganm95-linux-device-automount \
#     doganm95/linux-device-automount:latest
