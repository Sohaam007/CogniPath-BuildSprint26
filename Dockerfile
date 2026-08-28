FROM python:3.11-slim

# Install GCC and build tools for the C engine
RUN apt-get update && apt-get install -y gcc make && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Build the C library (Linux shared object)
WORKDIR /app/c_engine
RUN make

# Generate the synthetic data
WORKDIR /app/data_pipeline
RUN python generate_synthetic.py

# Switch back to the app root and set the command to run the FastAPI app
WORKDIR /app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]