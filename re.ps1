docker build -t automount .
docker run --device=/dev/sda1 -v /mnt:/mnt automount
