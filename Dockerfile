FROM python:3.9-slim

# Install required packages
RUN apt-get update \
    && apt-get install -y \
    udisks2

# Copy the Python script
COPY mount_usb.py /app/mount_usb.py

# Run the script
CMD ["python", "/app/mount_usb.py"]
