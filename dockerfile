FROM python:3.12-slim

WORKDIR /app
COPY inventorymanager.py .

# Store the data file in a folder that can be mounted as a volume
RUN mkdir -p /app/data
ENV INVENTORY_FILE=/app/data/inventory.json

CMD ["python", "inventorymanager.py"]