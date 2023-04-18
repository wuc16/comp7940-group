FROM python:latest
ENV ACCESS_TOKEN=6256944174:AAExNSezeuLiNzNsSPnyZo6RffDzGsoVLa4
ENV OPENAI_API=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
ENV FIREBASE=https://comp7940-group-default-rtdb.firebaseio.com/
WORKDIR /
COPY chatbot.py /
COPY requirements.txt /
COPY serviceAccount.json /
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt
CMD ["python", "chatbot.py"]