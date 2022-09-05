###########
# BUILDER #
###########
FROM clinicalgenomics/python3.8-venv:1.0 AS BUILDER

# Install and run commands from virtual environment
RUN python3 -m venv /home/worker/venv
ENV PATH="/home/worker/venv/bin:$PATH"

# install requirements
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

#########
# FINAL #
#########
FROM clinicalgenomics/python3.8-venv:1.0 AS DEPLOYER

RUN groupadd --gid 1000 worker && useradd -g worker --uid 1000 --create-home worker
COPY --chown=worker:worker --from=BUILDER /home/worker/venv /home/worker/venv

RUN mkdir /home/worker/app
WORKDIR /home/worker/app
COPY . .

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/worker/venv
ENV PATH="/home/worker/venv/bin:$PATH"

ENV GUNICORN_WORKERS=1
ENV GUNICORN_THREADS=1
ENV GUNICORN_BIND="0.0.0.0:8000"
ENV GUNICORN_TIMEOUT=400

CMD gunicorn \
    --workers=$GUNICORN_WORKERS \
    --worker-class=uvicorn.workers.UvicornWorker \
    --bind=$GUNICORN_BIND  \
    --threads=$GUNICORN_THREADS \
    --timeout=$GUNICORN_TIMEOUT \
    --proxy-protocol \
    --forwarded-allow-ips="10.0.2.100,127.0.0.1" \
    --log-syslog \
    --access-logfile - \
    --error-logfile - \
    --log-level="debug" \
    preClinVar.main:app
