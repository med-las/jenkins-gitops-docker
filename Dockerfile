# Use an official Odoo base image
FROM odoo:17

# Set the working directory in the container
WORKDIR /mnt/extra-addons

# Copy test script into the container
COPY test.py /mnt/extra-addons

# Install Python packages required for the test script
RUN pip3 install requests

# Expose the default Odoo port
EXPOSE 8069

# Run Odoo when the container launches
CMD ["odoo"]