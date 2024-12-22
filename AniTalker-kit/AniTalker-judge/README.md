# Judge

这一部分用于评价指标PSNR、SSIM、FID、NIQE的计算。

仓库中提供了代码、样例和Dockerfile文件，其中缺少了模型参数文件inception_v3_google-0cc3c7bd.pth，可以在[Google Drive](https://drive.google.com/file/d/1urWE3mUroo2rOn-A2nBXWhuKQ2I1M2zd/view?usp=drive_link)或[下载链接](https://download.pytorch.org/models/inception_v3_google-0cc3c7bd.pth)下载。

## Quick Start

1. 安装docker，宿主机CUDA版本为11.7及以上
2. 拉取镜像：

```
docker pull gre123/anitalkerjudge:v1
```

3. 参考以下docker run命令运行：

```
docker run --rm --gpus all \
-v your_stand_videos_dir_path:/app/stand_videos_dir_path \
-v your_generate_videos_dir_path:/app/generate_videos_dir_path \
gre123/anitalkerjudge:v1 \
/app/stand_videos_dir_path \
/app/generate_videos_dir_path
[--device your_device]（默认值为cuda:0）
```

其中，your_stand_videos_dir_path、your_generate_videos_dir_path为文件夹的绝对路径。
注意：评测程序会对两个文件夹中名称相同的视频进行评测指标的计算，运行该程序需要确保对应的参照视频和生成视频名称相同且时长相同。

## Install

如果想要自己手动构建镜像，请按照下列步骤进行：

1. 将项目代码拉取到本地

```
git clone https://github.com/RubyZh/talkingface-kit.git
cd talkingface-kit/AniTalker-kit/AniTalker-judge
```

2. 在项目根目录下打开终端，运行以下命令：

```
docker build --rm -f "Dockerfile" -t <image-name>:<tag> "."
```

如果ubuntu镜像无法拉取，可尝试先单独拉取对应镜像：

```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```

3. 构建成功后，参考上面的docker run命令运行。

## Run

如果想要直接在本地运行，请按照下列步骤进行：

1. 将项目代码拉取到本地
2. 打开Anaconda Prompt Shell，创建conda环境：

```
conda create -n AniTalker_judge python=3.9.21
conda activate AniTalker_judge
```

3. 安装依赖：

```
pip install -r requirements.txt
```

4. 将视频放到项目文件夹下，在项目根目录下运行：

```
python PSNR_SSIM_FID_NIQE.py /path/to/raw/video/dir /path/to/generate/video/dir
```
