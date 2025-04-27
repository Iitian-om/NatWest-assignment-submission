# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get remove -y gcc && apt-get autoremove -y && apt-get clean

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "app.py"]