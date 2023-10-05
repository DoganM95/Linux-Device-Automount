docker build -t automount .
docker run --privileged -v /mnt:/mnt automount