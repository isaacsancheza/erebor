FROM python:3.10.4-bullseye

ARG USERNAME=python
ARG USER_UID=1000
ARG USER_GID=1000
ARG WORKING_DIR=/app

# Create non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME

# Python requirements
COPY requirements.txt /tmp/pip-tmp/

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Create working directory
RUN mkdir $WORKING_DIR

RUN chown $USERNAME:$USERNAME -R $WORKING_DIR

# Use non-root user
USER $USERNAME

# Use working directory
WORKDIR $WORKING_DIR

CMD ["python"]
