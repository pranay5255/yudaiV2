FROM ghcr.io/sweagent/swe-rex:latest
WORKDIR /app
COPY . /app
EXPOSE 8000
CMD ["python", "main.py"]
