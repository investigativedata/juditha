FROM ghcr.io/investigativedata/ftm-docker:latest

COPY canonicaller /app/canonicaller
COPY setup.py /app/setup.py
COPY setup.cfg /app/setup.cfg
COPY pyproject.toml /app/pyproject.toml
COPY VERSION /app/VERSION
COPY README.md /app/README.md

WORKDIR /app
RUN pip install gunicorn uvicorn
RUN pip install .

USER 1000

ENTRYPOINT ["gunicorn", "canonicaller.api:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
