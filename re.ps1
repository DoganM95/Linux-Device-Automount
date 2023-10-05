docker build -t automount .
docker run --device=/dev/sda1 -v /dev:/dev -v /media:/media automount
