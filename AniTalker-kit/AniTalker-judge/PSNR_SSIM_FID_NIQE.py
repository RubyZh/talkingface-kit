import imageio
import torch
from pytorch_msssim import ssim
import numpy as np
from PIL import Image
import cv2
import pyiqa
from torchvision.models import inception_v3
from torchvision import transforms
import scipy.linalg as linalg
import warnings
import argparse
import os

# 忽略警告
warnings.filterwarnings('ignore')

# 加载视频帧
def load_video_frames(video_path):
    reader = imageio.get_reader(video_path)
    frames = [frame for frame in reader]
    reader.close()  # 关闭reader释放资源
    return frames

def resize_video(generated_frames, standard_size):
    resized_generated_frames = [cv2.resize(frame, (standard_size[1], standard_size[0])) for frame in generated_frames]
    return resized_generated_frames

# 计算PSNR
def calculate_psnr(standard_frames, generated_frames):
    psnr_values = []
    for i in range(len(standard_frames)):
        mse = np.mean((standard_frames[i] - generated_frames[i]) ** 2)
        if mse == 0:
            psnr = float('inf')  # 对于完全相同的图像，PSNR为无穷大
        else:
            max_pixel = 255.0
            psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        psnr_values.append(psnr)
    return np.mean(psnr_values)

# 计算SSIM
def calculate_ssim(standard_frames, generated_frames):
    ssim_values = []
    for i in range(len(standard_frames)):
        # 规范化帧数据到[0, 1]并转换为float32
        standard_frame = torch.tensor(standard_frames[i]).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        generated_frame = torch.tensor(generated_frames[i]).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        ssim_val = ssim(standard_frame, generated_frame, data_range=1.0, size_average=True)  # 正确的data_range
        ssim_values.append(ssim_val.item())
    return np.mean(ssim_values)

# 定义一个函数来提取视频帧的特征，使用批量处理
def extract_features(video_path, model, device, batch_size=16):
    frames = []
    cap = cv2.VideoCapture(video_path)
    batch = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img = transforms.ToTensor()(img).unsqueeze(0).to(device)
        batch.append(img)
        
        if len(batch) == batch_size:
            with torch.no_grad():
                batch_tensor = torch.cat(batch, dim=0)
                features = model(batch_tensor)
                frames.extend(features.cpu().numpy())
            batch = []  # 重置批量
        
    # 处理剩余的帧
    if batch:
        with torch.no_grad():
            batch_tensor = torch.cat(batch, dim=0)
            features = model(batch_tensor)
            frames.extend(features.cpu().numpy())
    
    cap.release()  # 释放视频捕获资源
    return frames

# 计算每个视频特征的均值和协方差
def calculate_statistics(features):
    mean = np.mean(features, axis=0)
    cov = np.cov(features, rowvar=False)
    return mean, cov

# 使用FID公式计算两个视频特征分布之间的FID分数
def calculate_fid(standard_mean, standard_cov, generated_mean, generated_cov):
    # 计算均值差
    mean_diff = standard_mean - generated_mean
    
    # 为了确保协方差矩阵正定，添加一个小的正则化项
    epsilon = 1e-6
    standard_cov += epsilon * np.eye(standard_cov.shape[0])
    generated_cov += epsilon * np.eye(generated_cov.shape[0])
    
    # 计算协方差矩阵的平方根
    cov_sqrt = linalg.sqrtm(standard_cov @ generated_cov)
    
    # 如果平方根返回复数，取其实部
    if np.iscomplexobj(cov_sqrt):
        cov_sqrt = cov_sqrt.real
    
    # 计算FID
    fid = np.sum(mean_diff ** 2) + np.trace(standard_cov + generated_cov - 2 * cov_sqrt)
    
    # 检查是否出现NaN或负值
    if np.isnan(fid) or fid < 0:
        fid = 0  # 或者返回一个合理的默认值
    return fid

# 计算NIQE得分
def calculate_niqe_score(frames):
    niqe_metric = pyiqa.create_metric('niqe')
    scores = []
    for frame in frames:
        frame_tensor = torch.from_numpy(frame).permute(2, 0, 1).unsqueeze(0).float() / 255.0  # 规范化到[0, 1]
        score = niqe_metric(frame_tensor)
        scores.append(score)
    del niqe_metric  # 删除NIQE指标以释放资源
    return torch.tensor(scores).mean().item()

# 定义评价函数
def evaluate_video(video_name, standard_path, generated_path, device):
    path_standard_video = os.path.join(standard_path, video_name)
    path_generated_video = os.path.join(generated_path, video_name)
    
    standard_frames = load_video_frames(path_standard_video)
    generated_frames = load_video_frames(path_generated_video)
    
    if generated_frames[0].shape != standard_frames[0].shape:
        generated_frames = resize_video(generated_frames, standard_frames[0].shape)
    
    psnr_score = round(calculate_psnr(standard_frames, generated_frames), 6)
    ssim_score = round(calculate_ssim(standard_frames, generated_frames), 6)
    
    standard_features = extract_features(path_standard_video, inception_model, device)
    generated_features = extract_features(path_generated_video, inception_model, device)
    
    standard_mean, standard_cov = calculate_statistics(standard_features)
    generated_mean, generated_cov = calculate_statistics(generated_features)
    
    fid_score = round(calculate_fid(standard_mean, standard_cov, generated_mean, generated_cov), 6)
    generated_niqe = round(calculate_niqe_score(generated_frames), 6)
    
    return psnr_score, ssim_score, fid_score, generated_niqe

# 命令行参数解析
parser = argparse.ArgumentParser(description='Evaluate videos using various metrics.')
parser.add_argument('stand_path', type=str, help='Path to the standard videos folder')
parser.add_argument('generate_path', type=str, help='Path to the generated videos folder')
parser.add_argument('--device', type=str, default='cuda:0', help='Device to use for computations (default: cuda:0)')
args = parser.parse_args()

# 视频路径
standard_videos_path = args.stand_path
generated_videos_path = args.generate_path
device = torch.device(args.device)


# 检查是否有可用的 GPU
if device.type == 'cuda' and not torch.cuda.is_available():
    raise ValueError("CUDA is not available, but device set to cuda. Please check your device settings.")


# 加载预训练的Inception模型

inception_model = inception_v3(pretrained=False)
inception_model.load_state_dict(torch.load('/app/inception_v3_google-0cc3c7bd.pth'))
inception_model.to(device).eval()


# 视频列表
standard_video_names = os.listdir(standard_videos_path)
generated_video_names = os.listdir(generated_videos_path)


# 获取两个列表的交集
video_names = list(set(standard_video_names) & set(generated_video_names))


# 输出指标名作为表头，设置列宽
header = "Video Name".ljust(20) + "PSNR Score".ljust(12) + "SSIM Score".ljust(12) + "FID Score".ljust(12) + "NIQE Score".ljust(12)
print(header)

# 循环处理每个视频
for video_name in video_names:
    psnr_score, ssim_score, fid_score, niqe_score = evaluate_video(video_name, standard_videos_path, generated_videos_path, device)
    
    # 格式化输出，确保列对齐
    row = f"{video_name.ljust(20)}{psnr_score:<12}{ssim_score:<12}{fid_score:<12}{niqe_score:<12}"
    print(row)

    # 释放不再需要的资源
    torch.cuda.empty_cache()  # 释放GPU缓存