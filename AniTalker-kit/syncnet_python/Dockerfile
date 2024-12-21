# 使用 NVIDIA 官方 CUDA 12.3 镜像作为基础镜像
FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 设置环境变量以避免交互式安装提示
ENV DEBIAN_FRONTEND=noninteractive

# 更新包索引并安装依赖项（包括 wget、git、Python 及其他工具）
RUN apt-get update && apt-get install -y \
    wget \
    git \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件到容器
COPY . /app

# 安装 Python 库依赖
RUN pip3 install -r requirements.txt

# 设置工作目录
WORKDIR /app

# 开放端口 8080，用于 Web 服务
EXPOSE 8080

# 运行你的应用程序
ENTRYPOINT ["python3", "demo.py"]