# Use a specific, stable Python version as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files
COPY requirements.txt requirements.txt
COPY packages.txt packages.txt

# Install system-level packages
RUN apt-get update && apt-get install -y --no-install-recommends $(cat packages.txt)

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- THIS IS THE KEY STEP ---
# Copy your pre-built ChromaDB folder into the container
COPY chroma_db ./chroma_db

# Copy the rest of your application code
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Define the command to run your app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]