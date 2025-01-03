# talkingface-kit

本项目基于[AniTalker](https://github.com/X-LANCE/AniTalker),[SyncNet](https://github.com/joonson/syncnet_python/tree/master)

项目包括三个部分：AniTalker、Judge和Syncnet


## AniTalker

项目通过身份解耦面部运动编码，实现音频、图片生成视频。

在原项目的基础上,进行了下列修改：

1. 修改code/demo.py代码，改变了接口的名称，保存为code/demo_final.py代码。
2. 在test_demo/portraits/中添加了May.png，在test_demo/audios/中添加了short_May.wav，用于测试封装后的镜像。
3. 新增了run_output文件夹，该文件夹为运行封装后的镜像时挂载的输出文件夹，其中的视频文件是通过运行封装后的镜像生成的视频。
4. 新增了Dockerfile，用于构建docker镜像。
5. 新增了run_main.txt，给出docker镜像的运行示例。
6. 修改了requirements.txt，修改了torch、torchvision、torchaudio的版本，以适配cuda11.7，增加了gfpgan包，以便在运行时使用 --face_sr参数，生成512*512的视频。
7. 新增了parsing_parsenet.pth，将模型参数保存在本地。

### Quick Start

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

### 更多食用方法

[AniTalker](https://github.com/RubyZh/talkingface-kit/blob/main/AniTalker-kit/AniTalker/README.md)

## Judge

用于计算生成视频的PSNR、SSIM、FID、NIQE，用于定量评估视频生成效果。

在计算PSNR、SSIM、NIQE时，分别计算每一帧的指标结果，再取平均值。

在计算FID时，对视频的每一帧利用inception_v3模型提取特征，将一个视频所有帧的特征向量求均值和协方差，进行计算。

### Quick Start

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

### 其他食用方法

[Judge](https://github.com/RubyZh/talkingface-kit/blob/main/AniTalker-kit/AniTalker-judge/README.md)

## Syncnet

用于计算生成视频的LSE-D LSE-C,用于定量评估生成视频效果，无需ground-truth

在原项目的基础上,进行了下列修改：

1. 增加了demo.py、Dockerfile，修改了calculate_scores_real_videos.sh,方便构建docker镜像，并在构建完成后使用docker命令直接获取评估结果。
2. 修改了代码中部分无法兼容numpy较高版本导致的问题（e.g. int32）
3. 修改了requirements.txt，提供了必要的、相对较高版本的依赖。

### Quick Start

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

### 更多食用方法

[Syncnet](https://github.com/RubyZh/talkingface-kit/blob/main/AniTalker-kit/syncnet_python/README.md)

## Questions

常见问题及解决方式可参考[Q&A](https://github.com/RubyZh/talkingface-kit/blob/main/AniTalker-kit/docs/Questions.md)

## Contributors

<a href="https://github.com/RubyZh/talkingface-kit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=RubyZh/talkingface-kit" />
</a>

Made with [contrib.rocks](https://contrib.rocks).