# AA Flight Scraper - Contest Submission
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Chrome in one layer (faster)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (excluding unnecessary files)
COPY contest_compliant_scraper.py .
COPY src/ ./src/
COPY .env .

# Set contest environment variables
ENV ORIGIN=LAX
ENV DESTINATION=JFK
ENV DATE=2025-12-15
ENV PASSENGERS=1
ENV CABIN_CLASS=economy
ENV HEADLESS=true
ENV OUTPUT_DIR=/app/output
ENV DOCKER_ENV=true
ENV CONTEST_MODE=true

# Create output directory
RUN mkdir -p /app/output

# Set display for headless Chrome
ENV DISPLAY=:99

# Chrome configuration for Docker
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

# Add Chrome arguments for Docker environment
ENV CHROME_ARGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --remote-debugging-port=9222"

# Entry point - run the contest scraper with xvfb
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & python contest_compliant_scraper.py"]