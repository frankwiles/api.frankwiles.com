FROM python:3.11-slim as builder-py

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt \
    apt update && \
    apt install -y build-essential git gcc python-dev libpq-dev

RUN --mount=type=cache,target=/root/.cache,id=pip \
    pip install -U pip

COPY ./requirements.txt ./code/requirements.txt

RUN python3 -m venv /venv

RUN --mount=type=cache,target=/root/.cache,id=pip \
    . /venv/bin/activate && \
    pip install -U pip pip-tools && \
    pip install -r /code/requirements.txt

RUN rm -f `find . -iname "*.c"` && \
    rm -f `find . -iname "*.pyc"` && \
    rm -f `find . -iname "*.pyx"` && \
    rm -rf `find . -iname "__pycache__"`

FROM python:3.11-slim AS release

ENV PATH /venv/bin:/bin:/usr/bin:/usr/local/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

RUN mkdir /code

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt \
    apt update && \
    apt install --no-install-recommends -y git libpq-dev

COPY --from=builder-py /venv/ /venv/
COPY . /code/

WORKDIR /code

CMD ["gunicorn", "-c", "/code/gunicorn.conf.py", "config.wsgi"]

ENV X_IMAGE_TAG v0.0.0

LABEL Description="AlphaKit Image" Vendor="REVSYS"
LABEL Version="${X_IMAGE_TAG}"
