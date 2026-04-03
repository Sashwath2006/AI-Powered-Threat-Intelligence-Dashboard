FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY frontend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY frontend /app

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
