FROM python:3.12-slim

# Working directory set karein
WORKDIR /app

# Zaroori system libraries (agar koi ho)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pura backend code copy karein
COPY . .

# Hugging Face Spaces hamesha port 7860 use karta hai
ENV PORT=7860
EXPOSE 7860

# start.sh ko executable banayein
RUN chmod +x start.sh

# App start karne ki command
CMD ["./start.sh"]
