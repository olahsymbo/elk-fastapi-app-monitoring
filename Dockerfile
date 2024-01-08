FROM python:3.9-slim
ENV PYTHONPATH=/usr/lib/python3.9/site-packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils libgl1 libglib2.0-0 \
    python3-pip \
    && apt-get install psmisc \
    && apt-get clean \
    && apt-get autoremove
RUN mkdir /elk-fastapi-app-monitoring
WORKDIR /elk-fastapi-app-monitoring
COPY . /elk-fastapi-app-monitoring
RUN pip3 install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root
EXPOSE 8000