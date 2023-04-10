FROM python:latest

WORKDIR /
COPY chatbot.py /
COPY requirements.txt /
COPY serviceAccount.json /
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt
CMD ["python", "chatbot.py"]