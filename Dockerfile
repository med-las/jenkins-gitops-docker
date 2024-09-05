FROM odoo:17

# Set the working directory
WORKDIR /mnt/extra-addons

# Optionally add your custom addons here if available
# COPY ./addons /mnt/extra-addons

# Optionally add any other configurations or scripts
# COPY test.py /mnt/test.py

# Install additional dependencies if needed
RUN apt-get update && apt-get install -y python3 python3-pip

# Command to run the Odoo server
CMD ["odoo"]
