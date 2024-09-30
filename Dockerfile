# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make sure pytest is installed
RUN pip install pytest

# Add pytest to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Command to run the application
CMD ["python", "app/main.py"]