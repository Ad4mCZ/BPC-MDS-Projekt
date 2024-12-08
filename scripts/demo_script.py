
# Importing required module
import os

os.system('echo "test python scriptu"')

stream_name1 = input("zadejte klíč streamu1:")
stream_name2 = input("zadejte klíč streamu2:")
stream_name3 = input("zadejte klíč streamu3:")
stream_name4 = input("zadejte klíč streamu4:")

print("klíč1 je: " + stream_name1)
print("klíč2 je: " + stream_name2)
print("klíč3 je: " + stream_name3)
print("klíč4 je: " + stream_name4)

#zavolání ffmpegu pro vytvoření streamů


ffmpeg = "ffmpeg "
input = "-stream_loop -1 -i /opt/mds/stream_inputs/"
R1080 = ''' -c:v libx264 -crf 30 -preset ultrafast -c:a copy -vf "drawtext=fontfile=arial.ttf:text='1080p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, fps=24"'''
R720 = ''' -c:v libx264 -crf 30 -preset ultrafast -c:a copy -b:a 192k -vf "drawtext=fontfile=arial.ttf:text='720p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:600, fps=24" -preset fast'''
R480 = ''' -c:v libx264 -crf 30 -preset ultrafast -c:a copy -b:a 128k -vf "drawtext=fontfile=arial.ttf:text='480p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:480, fps=24" -preset fast'''
R360 = ''' -c:v libx264 -crf 30 -preset ultrafast -c:a copy -b:a 64k -vf "drawtext=fontfile=arial.ttf:text='360p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20, scale=-2:320, fps=24" -preset fast'''
thumbnail = '''-vf "fps=1/10, scale=400:-1"''' + " /opt/mds/temp/thumbnails/"
out = " -f flv rtmp://localhost/hls/"

command1 = "-threads 16 " + input + "sample1.mp4" + R720 + " -map 0 " +  out + stream_name1 + "_720" + R480 + " -map 0 " + out + stream_name1 + "_480" + R720 + " -map 0 " + out + stream_name1 + "_360 " + " -map 0:v " + thumbnail + stream_name1 + "_thumbnail%03d.jpg "
command2 = input + "sample2.mp4" + R720 + " -map 1 " + out + stream_name2 + "_720" + R480 + " -map 1 " + out + stream_name2 + "_480" + R720 + " -map 1 " + out + stream_name2 + "_360 " + " -map 1:v " + thumbnail + stream_name2 + "_thumbnail%03d.jpg "
command3 = input + "sample3.mp4" + R720 + " -map 2 " + out + stream_name3 + "_720" + R480 + " -map 2 " + out + stream_name3 + "_480" + R720 + " -map 2 " + out + stream_name3 + "_360 " + " -map 2:v " + thumbnail + stream_name3 + "_thumbnail%03d.jpg "
command4 = input + "sample4.mp4" + R720 + " -map 3 " + out + stream_name4 + "_720" + R480 + " -map 3 " + out + stream_name4 + "_480" + R720 + " -map 3 " + out + stream_name4 + "_360 " + " -map 3:v " + thumbnail + stream_name4 + "_thumbnail%03d.jpg "
command = ffmpeg + command1 + command2 + command3
print(command)
os.system(command)
