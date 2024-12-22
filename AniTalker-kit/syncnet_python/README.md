# SyncNet

本项目基于[SyncNet](https://github.com/joonson/syncnet_python/tree/master)

## Change
本项目在原项目的基础上,进行了下列修改：

1. 增加了demo.py、Dockerfile，修改了calculate_scores_real_videos.sh,方便构建docker镜像，并在构建完成后使用docker命令直接获取评估结果。
2. 修改了代码中部分无法兼容numpy较高版本导致的问题（e.g. int32）
3. 修改了requirements.txt，提供了必要的、相对较高版本的依赖。

## Quick Start
1. 安装docker，宿主机CUDA版本为11.7及以上
2. 从Dockerhub拉取构建好的镜像
```
docker pull bellacora/syncnet-image:v4
```
3. 拉取镜像后使用docker命令运行（如果为本地运行加 --gpus all）
```
docker run --rm --gpus all -v path:/app/videos --folderpath /app/videos
```
其中path部分应当替换为宿主机上视频文件夹（注意是文件夹）的绝对路径，将会评估文件夹内所有视频，并按照文件夹内视频名称的字典顺序输出评估结果

4. 输出结果的最后X行（文件夹内有X个视频）为计算的LSE-D LSE-C值，按照文件夹内视频名称的字典顺序输出

## Install
如果想要自己手动构建镜像，请按照下列步骤进行：
1. 将项目代码拉取到本地
2. 在项目根目录下打开终端，运行
```
docker build -t <image-name> .
```
如果ubuntu镜像无法拉取，可尝试先单独拉取对应镜像。
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```
该镜像可以尝试修改为对应的CUDA版本（同时修改Dockerfile中相关版本及对应的依赖）

如果requirements.txt内的依赖在电脑上无法兼容，可尝试调整torch和torchvision的版本，以便与CUDA版本兼容；但scenedetect的版本不能低于0.6.0，其他依赖版本依照原项目中给出的，应当满足torch>=1.4.0,torchvision>=0.5.0,numpy>=1.18.1,scipy>=1.2.1

3. 运行成功后，使用docker命令运行，参考前述命令标准

## 
如果不通过docker，直接运行，请按照下列步骤进行：
1. 将项目代码拉取到本地
```
git clone https://github.com/RubyZh/talkingface-kit.git
cd talkingface-kit/AniTalker-kit/syncnet_python
```
2. 打开Anaconda Prompt Shell,运行
```
conda create -n syncnet python=3.9.0
conda activate syncnet
```
3. 安装必要依赖
```
pip install -r requirements.txt
```
4. 将视频放至文件夹下，运行代码
```
sh calculate_scores_real_videos.sh /path/to/video/data/root
```
在calculate_scores_real_videos.sh文件内，ls 命令默认按字典顺序列出文件，因此，$yourfilenames 中的文件会按照字典顺序排列，输出结果按照字典顺序排列