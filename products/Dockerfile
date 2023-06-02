FROM python:3.9

WORKDIR /app

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=productservice.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
