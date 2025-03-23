# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Create a writable cache directory
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Set the environment variable to use this directory
ENV TRANSFORMERS_CACHE=/app/cache

# Install fontconfig
RUN apt-get update && apt-get install -y fontconfig

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for FastAPI (8000) and Streamlit (7860)
EXPOSE 8000
EXPOSE 7860

# Start both FastAPI and Streamlit
CMD ["bash", "-c", "uvicorn api:app --host 127.0.0.1 --port 8000 & streamlit run app.py --server.port 7860 --server.address 0.0.0.0"]