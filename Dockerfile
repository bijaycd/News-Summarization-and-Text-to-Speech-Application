# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Create writable cache directories for Matplotlib & Fontconfig
RUN mkdir -p /app/cache && chmod -R 777 /app/cache
RUN mkdir -p /root/.config/matplotlib && chmod -R 777 /root/.config/matplotlib
RUN mkdir -p /root/.cache/fontconfig && chmod -R 777 /root/.cache/fontconfig

# Set environment variables for caching
ENV TRANSFORMERS_CACHE=/app/cache
ENV MPLCONFIGDIR=/root/.config/matplotlib
ENV XDG_CACHE_HOME=/root/.cache

# Install required system dependencies
RUN apt-get update && apt-get install -y fontconfig

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for FastAPI (8000) and Streamlit (7860)
EXPOSE 8000
EXPOSE 7860

# Run both FastAPI and Streamlit properly
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 7860 --server.address 0.0.0.0