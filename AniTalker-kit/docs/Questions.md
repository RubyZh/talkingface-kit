# 常见问题及解决方案

## AniTalker

1. 模型权重下载失败
如果无法下载模型权重，也能够生成256×256的视频，可以删除Dockerfile对应的COPY命令
```
COPY detection_Resnet50_Final.pth /app/gfpgan/weights/detection_Resnet50_Final.pth
COPY GFPGANv1.4.pth /usr/local/lib/python3.9/dist-packages/gfpgan/weights/GFPGANv1.4.pth
```
随后构建镜像

## Judge

## Syncnet

1. ubuntu镜像无法拉取，可尝试先单独拉取对应镜像
```
docker pull nvidia/cuda:11.7.1-runtime-ubuntu22.04
```
