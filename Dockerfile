FROM ubuntu:20.04

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    tesseract-ocr-ara \
    poppler-utils \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# إنشاء رابط رمزي لبايثون
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

# نسخ متطلبات بايثون
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
# تثبيت متطلبات بايثون
RUN pip3 install --no-cache-dir -r requirements.txt

# نسخ ملفات التطبيق
COPY . .

CMD ["python", "app.py"]
