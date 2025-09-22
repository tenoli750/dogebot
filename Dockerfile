FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_crypto_bot.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_crypto_bot.txt

# Copy bot files
COPY top100_crypto_bot.py .
COPY crypto_bot.env .

# Create non-root user
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://api.coingecko.com/api/v3/ping')" || exit 1

# Run the bot
CMD ["python", "top100_crypto_bot.py"]
