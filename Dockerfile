# Dasarnya tetap image resmi Odoo 17
FROM odoo:17

# Perlu jadi root dulu untuk install sesuatu ke sistem
USER root


RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-roboto \
    fonts-noto \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*


# Kembali ke user odoo
USER odoo