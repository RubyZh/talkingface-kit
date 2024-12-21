import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EchoMimic')
    parser.add_argument('--folderpath', type=str, required=True, help="Path to videos")
    args = parser.parse_args()

    command = f"sh calculate_scores_real_videos.sh '{args.folderpath}'"
    os.system(command)