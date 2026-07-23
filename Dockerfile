FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alarm_clock/ ./alarm_clock/

CMD ["python", "-m", "alarm_clock"]
