
# Importing required module
import os

os.system('echo "test python scriptu"')

stream_name1  = "jirka2"

print("klíč je: " + stream_name1)

#zavolání ffmpegu pro vytvoření streamů


ffmpeg = "ffmpeg "
input = "-i rtmp://localhost:1935/hls/" 
R1080 = ''' -c:v libx264 -c:a aac -b:a 256k -vf "drawtext=fontfile=arial.ttf:text='1080p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20"'''
R720 = ''' -c:v libx264 -c:a aac -b:a 192k -vf "drawtext=fontfile=arial.ttf:text='720p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:720" -preset fast'''
R480 = ''' -c:v libx264 -c:a aac -b:a 128k -vf "drawtext=fontfile=arial.ttf:text='480p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:480" -preset fast'''
R360 = ''' -c:v libx264 -c:a aac -b:a 64k -vf "drawtext=fontfile=arial.ttf:text='360p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:360" -preset fast'''
thumbnail = "-vf fps=1/60" + " /opt/mds/temp/tmp_hls/"
out = " -f flv rtmp://localhost/hls/"

command1 = "-threads 4 " + input + stream_name1 + " -async 1 -vsync -1" + R720 + " -map 0 " +  out + stream_name1 + "_720" + R480 + " -map 0 " + out + stream_name1 + "_480" + R720 + " -map 0 " + out + stream_name1 + "_360 " + " -map 0:v " + thumbnail + stream_name1 + "_thumbnail%03d.jpg "
command = ffmpeg + command1
print(command)
os.system(command)
