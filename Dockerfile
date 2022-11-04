FROM python:3.10.8-slim-bullseye AS py

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install -e .

ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=true

EXPOSE 8000
EXPOSE 5000

CMD ["flask", "run"]
# CMD [ "python", "simulation.py" ]