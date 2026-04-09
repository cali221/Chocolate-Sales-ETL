ARG PYTHON_VERSION=3.10.3
FROM python:${PYTHON_VERSION}-slim 

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# install git (needed for dbt)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

ARG UID=1000
ARG GID=1000

RUN addgroup --gid $GID appuser

# Create a non-privileged user that the app will run under
RUN adduser \
    --disabled-password \
    --gecos "" \
    --no-create-home \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    --gid "$GID" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

WORKDIR /choco-project-transform

RUN chown -R appuser:appuser /choco-project-transform

# Copy the source code into the container.
COPY --chown=appuser . .

# Switch to the non-privileged user to run the application.
USER appuser

RUN echo "Build UID is: $UID"

RUN echo "Build GID is: $GID"

# Expose the port that the docs webserver listens on
EXPOSE 8080

# Run the application.
CMD ["dbt", "build"]

# keep container up for development
#CMD ["tail", "-f", "/dev/null"]