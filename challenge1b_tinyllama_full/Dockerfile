# Use a base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

RUN apt-get update && apt-get install -y git curl build-essential

# Install required packages
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 --retries=5 -r requirements.txt


# Set environment variable for nltk_data
ENV NLTK_DATA=/app/nltk_data

# Download punkt to that location
RUN mkdir -p /app/nltk_data && \
    python -c "import nltk; nltk.download('punkt', download_dir='/app/nltk_data')"
# Run the app
CMD ["python", "main.py"]

