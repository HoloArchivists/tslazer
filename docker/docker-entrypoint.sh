ffmpeg -hide_banner -version
echo '---'
python /app/tslazer.py --path /data $@
