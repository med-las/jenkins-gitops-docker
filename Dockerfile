FROM odoo:17

# Install Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /mnt/extra-addons

# Copy files into the container
COPY . /mnt/extra-addons

# Set default command
CMD ["python3", "/mnt/extra-addons/test.py"]
