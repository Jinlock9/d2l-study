# D2L Study Environment

Docker environment for the PyTorch edition of [Dive into Deep Learning](https://d2l.ai/).

## Requirements

- Docker Desktop installed and running
- Working network access to Docker Hub and PyPI
- Project directory: `/Users/mac/Workspace/d2l-study`

## Environment

- Python 3.10
- PyTorch 2.0.0 (CPU)
- torchvision 0.15.1
- D2L 1.0.3
- JupyterLab
- Linux x86-64 container

On Apple Silicon, the container runs through emulation.

## 1. Create the Dockerfile

```bash
cd /Users/mac/Workspace/d2l-study

cat > Dockerfile <<'EOF'
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl unzip libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && python -m pip install \
       torch==2.0.0 torchvision==0.15.1 \
       --index-url https://download.pytorch.org/whl/cpu \
    && python -m pip install d2l==1.0.3 jupyterlab ipykernel \
    && python -m pip check

WORKDIR /workspace

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
EOF
```

## 2. Build the Image

```bash
docker build --platform linux/amd64 -t d2l-study .
```

Wait until the build succeeds before proceeding.

## 3. Create the Container

Run this once:

```bash
docker run -d \
    --platform linux/amd64 \
    --name d2l-study \
    -p 127.0.0.1:8888:8888 \
    --mount "type=bind,source=/Users/mac/Workspace/d2l-study,target=/workspace" \
    --shm-size=2g \
    d2l-study
```

The project directory is mounted at `/workspace`. Changes made there persist on the Mac.

## 4. Download the Book’s Notebooks

Run this once:

```bash
docker exec d2l-study bash -lc '
    curl -fL https://d2l.ai/d2l-en-1.0.3.zip -o /tmp/d2l.zip &&
    unzip -q /tmp/d2l.zip -d /workspace/notebooks
'
```

The PyTorch notebooks are located at:

| Location | Path |
|---|---|
| Mac | `/Users/mac/Workspace/d2l-study/notebooks/pytorch` |
| Container | `/workspace/notebooks/pytorch` |

## 5. Open JupyterLab

Print the server URL:

```bash
docker exec d2l-study jupyter server list
```

Open the URL in your browser. Replace the hostname with `127.0.0.1` if necessary, preserving the token:

```text
http://127.0.0.1:8888/lab?token=<token>
```

Navigate to `notebooks/pytorch` and open a notebook.

## 6. Verify Installation

```bash
docker exec d2l-study python -c \
'import torch; from d2l import torch as d2l; print(torch.__version__); print(torch.relu(torch.tensor([-1., 0., 1.])))'
```

Expected output:

```text
2.0.0+cpu
tensor([0., 0., 1.])
```

## Daily Usage

Start the existing container:

```bash
docker start d2l-study
```

Get the Jupyter URL:

```bash
docker exec d2l-study jupyter server list
```

Enter a container terminal:

```bash
docker exec -it d2l-study bash
```

Run a Python script from the project directory:

```bash
docker exec -it d2l-study python /workspace/example.py
```

Stop the container:

```bash
docker stop d2l-study
```

## Troubleshooting

### Docker daemon is not running

Start Docker Desktop:

```bash
open -a Docker
```

Wait until Docker Desktop reports that the engine is running, then retry.

### Docker Hub connection timeout

Check VPN/proxy settings. A VPN configuration issue previously caused a timeout while connecting to `auth.docker.io`.

Test connectivity:

```bash
curl -I --connect-timeout 10 https://auth.docker.io/
```

An HTTP response, including `404`, means the connection succeeded.

After resolving network access:

```bash
docker pull --platform linux/amd64 python:3.10-slim &&
docker build --platform linux/amd64 -t d2l-study .
```

### Image not found / pull access denied

The local image may not have been built successfully. Build it before running the container:

```bash
docker build --platform linux/amd64 -t d2l-study .
```

### Container name already exists

Start the existing container:

```bash
docker start d2l-study
```

### Inspect status and logs

```bash
docker ps -a --filter name=d2l-study
docker logs --tail 50 d2l-study
```

## Rebuild After Changing the Dockerfile

```bash
cd /Users/mac/Workspace/d2l-study

docker build --platform linux/amd64 -t d2l-study .
```

After the build succeeds, replace the container:

```bash
docker stop d2l-study
docker rm d2l-study

docker run -d \
    --platform linux/amd64 \
    --name d2l-study \
    -p 127.0.0.1:8888:8888 \
    --mount "type=bind,source=/Users/mac/Workspace/d2l-study,target=/workspace" \
    --shm-size=2g \
    d2l-study
```

Files in the mounted project directory are preserved. Files and packages created elsewhere inside the old container are removed.

## References

- [Dive into Deep Learning](https://d2l.ai/)
- [Official installation instructions](https://d2l.ai/chapter_installation/index.html)