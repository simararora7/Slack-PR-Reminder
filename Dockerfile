FROM python:2-alpine

WORKDIR /home/pull

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./slack_pull_reminder.py" ]