# 使用nvidia的CUDA基础镜像
FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 安装依赖，同时设置非交互式前端和时区
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    libgl1-mesa-glx \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 升级pip到最新版本，确保使用的是python3.9的pip
RUN python3.9 -m pip install --upgrade pip

# 设置Python版本为3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1


# 安装Python依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# 将Python脚本复制到容器中
COPY PSNR_SSIM_FID_NIQE.py /app/PSNR_SSIM_FID_NIQE.py

COPY inception_v3_google-0cc3c7bd.pth /app/inception_v3_google-0cc3c7bd.pth
COPY niqe_modelparameters.mat /root/.cache/torch/hub/pyiqa/niqe_modelparameters.mat

# 使脚本可执行
RUN chmod +x /app/PSNR_SSIM_FID_NIQE.py

# 设置CUDA_HOME环境变量
ENV CUDA_HOME=/usr/local/cuda

# 运行脚本
ENTRYPOINT ["python3.9", "/app/PSNR_SSIM_FID_NIQE.py"]

