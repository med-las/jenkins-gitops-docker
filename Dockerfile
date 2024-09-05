# Use an official Odoo base image
FROM odoo:17

# Set the working directory in the container
WORKDIR /mnt/extra-addons

# Expose the default Odoo port
EXPOSE 8069

# Run Odoo when the container launches
CMD ["odoo"]
