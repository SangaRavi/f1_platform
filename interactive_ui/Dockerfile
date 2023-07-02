FROM python:3.9 AS compile-image
RUN apt-get update -y && mkdir /app && python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY . /app
WORKDIR /app
RUN pip install -r requirements-frontend.txt

FROM python:3.9 AS run-image
RUN apt-get update -y && mkdir /app
COPY --from=compile-image /app /app
ENV PATH="/app/venv/bin:$PATH"
ENV BACKEND_ENV="backend"
WORKDIR /app

ENTRYPOINT [ "streamsync", "run" ]
EXPOSE 3005
CMD [ "ui",  "--port", "3005", "--host", "0.0.0.0" ]