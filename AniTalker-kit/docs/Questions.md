# 常见问题及解决方案

## AniTalker

1. 模型权重下载失败
如果无法下载模型权重，也能够生成512×512的视频（运行时自动下载），可以删除Dockerfile对应的COPY命令
```
COPY detection_Resnet50_Final.pth /app/gfpgan/weights/detection_Resnet50_Final.pth
COPY GFPGANv1.4.pth /usr/local/lib/python3.9/dist-packages/gfpgan/weights/GFPGANv1.4.pth
```
随后构建镜像

2. 如果在本地不使用docker运行，可以打开web窗口进行视频生成。

也可以使用命令行:
```
python demo_final.py \
--input_image image_path \
--input_audio_text audio_path \
--output_dir output_dir_path 
[--face_sr]（没有该参数时生成256*256的视频，加上该参数后生成512*512的视频）
[--device your_device]（默认值为cuda:0）
```
(上述路径均为绝对路径)

3. ubuntu镜像无法拉取，可尝试先单独拉取对应镜像
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```
4. 检查点ckpts下载失败，使用huggingface镜像源进行下载[huggingface](https://hf-mirror.com/taocode/anitalker_ckpts)

5. 安装 dlib 时，构建其所需的 wheel 失败

核心原因是 dlib 的构建需要 CMake，但系统中未安装 CMake，或 CMake 没有正确配置。

解决步骤如下：

(1) 安装 CMake：在系统中安装 CMake，根据操作系统选择合适的安装方法。从CMake Download官方网站中下载对应版本并进行安装即可，安装时注意勾选添加到环境变量。

(2) 安装构建工具（Windows）：由于使用的是 Windows，dlib 还需要 Microsoft C++ Build Tools。下载 Microsoft C++ 生成工具 - Visual Studio，在安装向导中选择 C++ Desktop Development 工作负载

(3) 安装完成后，重新打开终端

6. 执行 python code/webgui.py 并选择mp3格式的音频文件时出现报错

原因是系统中缺少 ffmpeg，gradio 库在尝试加载非 WAV 格式的音频文件时依赖于 ffmpeg

解决方法：在官网 [ffmpeg](https://ffmpeg.org) 下载ffmpeg，安装时勾选添加到环境变量，随后重新打开终端

## Judge

1. 模型权重下载失败

如果无法下载模型权重，也能够进行计算（运行时自动下载），可以删除Dockerfile对应的COPY命令
```
COPY inception_v3_google-0cc3c7bd.pth /app/inception_v3_google-0cc3c7bd.pth
```
随后构建镜像

2. ubuntu镜像无法拉取，可尝试先单独拉取对应镜像
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```

## Syncnet

1. ubuntu镜像无法拉取，可尝试先单独拉取对应镜像
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```
2. 本地运行时需要ffmpeg, 在官网 [ffmpeg](https://ffmpeg.org) 下载ffmpeg，安装时勾选添加到环境变量，随后重新打开终端
