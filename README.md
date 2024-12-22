# talkingface-kit

本项目基于[AniTalker](https://github.com/X-LANCE/AniTalker),[SyncNet](https://github.com/joonson/syncnet_python/tree/master)

项目包括三个部分：AniTalker、Judge和Syncnet

## AniTalker

项目通过身份解耦面部运动编码，实现音频、图片生成视频。

在原项目的基础上,进行了下列修改：

## Judge

## Syncnet

用于计算生成视频的LSE-D LSE-C,用于定量评估生成视频效果，无需ground-truth

在原项目的基础上,进行了下列修改：

1. 增加了demo.py、Dockerfile，修改了calculate_scores_real_videos.sh,方便构建docker镜像，并在构建完成后使用docker命令直接获取评估结果。
2. 修改了代码中部分无法兼容numpy较高版本导致的问题（e.g. int32）
3. 修改了requirements.txt，提供了必要的、相对较高版本的依赖。
