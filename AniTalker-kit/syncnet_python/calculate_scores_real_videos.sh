yourfilenames=`ls $1`

for eachfile in $yourfilenames
do
   python3 run_pipeline.py --videofile $1/$eachfile --reference wav2lip --data_dir tmp_dir
   python3 calculate_scores_real_videos.py --videofile $1/$eachfile --reference wav2lip --data_dir tmp_dir
done
