# Use an official lightweight Python image as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy just the requirements.txt first (this makes building faster if requirements don't change)
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the current directory contents into the container at /app
COPY . .

# Tell Docker to run the chatbot in interactive mode when the container starts
CMD ["python", "-m", "src.main", "--interactive"]
