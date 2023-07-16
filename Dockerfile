FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python3", "./tg_bot.py"]