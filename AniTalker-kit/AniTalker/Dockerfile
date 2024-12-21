# 使用 nvidia/cuda:11.7.1-runtime-ubuntu22.04 作为基础镜像
FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive



# 更新APT源为官方Ubuntu源并安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    libboost-all-dev \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*  # 清理apt缓存，以减少镜像大小

# 安装 Python 3.9
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y python3.9 python3.9-dev python3.9-distutils

# 安装指定版本的 pip 23.1
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9 && \
    python3.9 -m pip install --upgrade pip==23.1

# 检查 pip3.9 是否存在并设置 python 和 pip 为默认版本
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 \
    && ln -sf /usr/local/bin/pip3 /usr/bin/pip \
    && update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3 1

# 复制 requirements.txt 到容器中
COPY requirements.txt /app/requirements.txt

COPY detection_Resnet50_Final.pth /app/gfpgan/weights/detection_Resnet50_Final.pth

COPY parsing_parsenet.pth /app/gfpgan/weights/parsing_parsenet.pth

COPY GFPGANv1.4.pth /usr/local/lib/python3.9/dist-packages/gfpgan/weights/GFPGANv1.4.pth


# 安装其他 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器中
COPY . /app

# 暴露容器端口（根据需要设置）
EXPOSE 3001

# 设置默认执行命令（根据项目实际情况修改）
ENTRYPOINT ["python", "code/demo_final.py"]
