# talkingface-kit

本项目基于[AniTalker](https://github.com/X-LANCE/AniTalker),[SyncNet](https://github.com/joonson/syncnet_python/tree/master)

## AniTalker

项目通过身份解耦面部运动编码，实现音频、图片生成视频。

在原项目的基础上,进行了下列修改：

1. 修改code/demo.py代码，改变了接口的名称，保存为code/demo_final.py代码。
2. 在test_demo/portraits/中添加了May.png，在test_demo/audios/中添加了short_May.wav，用于测试封装后的镜像。
3. 新增了run_output文件夹，该文件夹为运行封装后的镜像时挂载的输出文件夹，其中的视频文件是通过运行封装后的镜像生成的视频。
4. 新增了Dockerfile，用于构建docker镜像。
5. 新增了run_main.txt，给出docker镜像的运行示例。
6. 修改了requirements.txt，修改了torch、torchvision、torchaudio的版本，以适配cuda11.7，增加了gfpgan包，以便在运行时使用 --face_sr参数，生成512*512的视频。

## Judge

用于计算生成视频的PSNR、SSIM、FID、NIQE，用于定量评估视频生成效果。

## Syncnet

用于计算生成视频的LSE-D LSE-C,用于定量评估生成视频效果，无需ground-truth

在原项目的基础上,进行了下列修改：

1. 增加了demo.py、Dockerfile，修改了calculate_scores_real_videos.sh,方便构建docker镜像，并在构建完成后使用docker命令直接获取评估结果。
2. 修改了代码中部分无法兼容numpy较高版本导致的问题（e.g. int32）
3. 修改了requirements.txt，提供了必要的、相对较高版本的依赖。
