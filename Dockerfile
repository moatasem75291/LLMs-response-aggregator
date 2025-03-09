# Use the selenium/standalone-chrome base image
FROM selenium/standalone-chrome:134.0

# Switch to root user to install dependencies
USER root

# Install specific version of Python (3.10) and related tools
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    build-essential \
    libffi-dev \
    xvfb \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure Python 3.10 is the default python3
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/bin/python3.10 /usr/bin/python

# Set Python-related environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Create a virtual environment and install pip within it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip directly in the virtual environment
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | /opt/venv/bin/python

# Set the working directory in the container
WORKDIR /app

# 🚨🚨 OPTIONAL STEP: Set environment variables for DeepSeek credentials if you want to use
# Only use this step if you want to set your DeepSeek credentials.
RUN echo -e "DEEPSEEK_EMAIL=\"PUT-YOUR-EMAIL-HERE\"\nDEEPSEEK_PASSWORD=\"PUT-YOUR-PASS-HERE\"" > .env

# Copy the application files and install Python dependencies
COPY requirements.txt .
# Use the virtual environment's pip to install dependencies
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt_tab'); nltk.download('punkt'); nltk.download('stopwords', quiet=True)"

# Copy the rest of the application files
COPY . .

# Ensure correct permissions for /tmp/.X11-unix to prevent Xvfb warnings
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Create directory for undetected_chromedriver and set permissions
RUN mkdir -p /home/seluser/.local/share/undetected_chromedriver \
    && chown -R seluser:seluser /home/seluser/.local

# Change ownership of venv and app directory to seluser
RUN chown -R seluser:seluser /opt/venv /app

# Switch to seluser (default user in selenium/standalone-chrome)
USER seluser

# Expose the application port (FastAPI default is 8000)
EXPOSE 8000

# Start Xvfb and run the FastAPI application
CMD ["sh", "-c", "Xvfb :99 -ac 2>/dev/null & uvicorn main:app --host 0.0.0.0 --port 8000"]