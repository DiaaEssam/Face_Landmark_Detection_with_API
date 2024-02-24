FROM python:3.9.18

WORKDIR /usr/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./API.py"]