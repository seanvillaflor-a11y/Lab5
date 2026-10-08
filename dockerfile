FROM python:3.12-slim

WORKDIR /app
COPY inventory_manager.py .

# Store the data file in a folder that can be mounted as a volume
RUN mkdir -p /app/data
ENV INVENTORY_FILE=/app/data/inventory.json

CMD ["python", "inventory_manager.py"]