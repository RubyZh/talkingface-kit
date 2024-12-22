# AniTalker

项目基于[AniTalker](https://github.com/X-LANCE/AniTalker)

## Change

项目通过身份解耦面部运动编码，实现音频、图片生成视频。

在原项目的基础上,进行了下列修改：

1. 修改code/demo.py代码，改变了接口的名称，保存为code/demo_final.py代码。
2. 在test_demo/portraits/中添加了May.png，在test_demo/audios/中添加了short_May.wav，用于测试封装后的镜像。
3. 新增了run_output文件夹，该文件夹为运行封装后的镜像时挂载的输出文件夹，其中的视频文件是通过运行封装后的镜像生成的视频。
4. 新增了Dockerfile，用于构建docker镜像。
5. 新增了run_main.txt，给出docker镜像的运行示例。
6. 修改了requirements.txt，修改了torch、torchvision、torchaudio的版本，以适配cuda11.7，增加了gfpgan包，以便在运行时使用 --face_sr参数，生成512*512的视频。
7. 新增了parsing_parsenet.pth，将模型参数保存在本地。

## Quick Start

1. 安装docker，宿主机CUDA版本为11.7及以上
2. 从Dockerhub拉取构建好的镜像
```
docker pull gre123/anitalkermodel:v1
```
3. 拉取镜像后使用docker命令运行（如果为本地运行加 --gpus all）
```
docker run --rm –gpus all \
-v your_image_path:/app/image_path \
-v your_audio_path:/app/audio_path \
-v your_output_dir_path:/app/output_dir_path \
gre123/anitalkermodel:v1 \
--input_image /app/image_path \
--input_audio_text /app/audio_path \
--output_dir /app/output_dir_path
[--face_sr]（没有该参数时生成256*256的视频，加上该参数后生成512*512的视频）
[--device your_device]（默认值为cuda:0）
```
其中，your_image_path、your_audio_path为文件的绝对路径，your_output_dir_path为文件夹的绝对路径。

例如：
```
docker run --rm --gpus all --memory="64g" --cpus="4" -v F:/AniTalker/AniTalker-main/test_demos/portraits/May.png:/app/May.png -v F:/AniTalker/AniTalker-main/test_demos/audios/short_May.wav:/app/short_May.wav -v F:/AniTalker/AniTalker-main/run_output:/app/run_output gre123/anitalkermodel:v1 --input_image /app/May.png --input_audio_text /app/short_May.wav --output_dir /app/run_output
```

4. 生成视频可在对应文件夹下查看

## Install

如果想要自己手动构建镜像，请按照下列步骤进行：

1. 将项目代码拉取到本地
```
git clone https://github.com/RubyZh/talkingface-kit.git
cd talkingface-kit/AniTalker-kit/AniTalker
```
2. 下载检查点
```
git lfs install
git clone https://huggingface.co/taocode/anitalker_ckpts ckpts
```
3. 下载模型权重 [GFPGANv1.4.pth](https://drive.google.com/file/d/1cVAYvvMJQoX9Jbvj08EiWDOJzRWBhL1V/view?usp=drive_link),[detection_Resnet50_Final.pth](https://drive.google.com/file/d/13P3bCDXAAFvcQ5lxkzlby11U0WFZpymF/view?usp=drive_link),将文件放至AniTalker根目录下

4. 在项目根目录下打开终端，运行
```
docker build -t <image-name> .
```
如果ubuntu镜像无法拉取，可尝试先单独拉取对应镜像。
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```
该镜像可以尝试修改为对应的CUDA版本（同时修改Dockerfile中相关版本及对应的依赖）

5. 运行成功后，使用docker命令运行

## Run

如果不通过docker，直接运行，请按照下列步骤进行：

1. 将项目代码拉取到本地
```
git clone https://github.com/RubyZh/talkingface-kit.git
cd talkingface-kit/AniTalker-kit/AniTalker
```
2. 打开Anaconda Prompt,运行
```
conda create -n anitalker python=3.9.0
conda activate anitalker
```
3. 安装必要依赖
```
pip install -r requirements.txt
```
4. 下载检查点
```
git lfs install
git clone https://huggingface.co/taocode/anitalker_ckpts ckpts
```
5. 下载模型权重 [GFPGANv1.4.pth](https://drive.google.com/file/d/1cVAYvvMJQoX9Jbvj08EiWDOJzRWBhL1V/view?usp=drive_link),[detection_Resnet50_Final.pth](https://drive.google.com/file/d/13P3bCDXAAFvcQ5lxkzlby11U0WFZpymF/view?usp=drive_link),将文件放至AniTalker根目录下

6. 运行,打开web界面交互
```
python code/webgui.py
```
