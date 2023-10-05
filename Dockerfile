FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    util-linux \
    e2fsprogs \
    && apt-get clean

# Copy the Python script
COPY automount.py /app/automount.py

# Run the script
CMD ["python", "/app/automount.py"]