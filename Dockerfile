FROM python:3.9-slim

COPY automount.py /automount.py

CMD ["python", "/automount.py"]
