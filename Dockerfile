FROM odoo:17

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install requests

# Set the working directory
WORKDIR /mnt/extra-addons

# Copy files into the container
COPY . /mnt/extra-addons

# Set default command to run the test script
CMD ["python3", "/mnt/extra-addons/test.py"]