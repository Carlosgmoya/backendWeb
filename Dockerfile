# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /parcial2

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Define the command to run the application
CMD ["python", "-m", "uvicorn", "main:api", "--reload", "--host", "0.0.0.0", "--port", "8001"]