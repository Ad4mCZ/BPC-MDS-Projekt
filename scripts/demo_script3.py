


# Importing required module
import os
import threading
import subprocess
import time

os.system('echo "test python scriptu"')

stream_name1  = "jirka3"

print("klíč je: " + stream_name1)


def run_ffmpeg(output_name):
    # Definice příkazu FFmpeg s dynamickým názvem výstupu
    command = [
        "ffmpeg",
        "-threads", "4",
        "-stream_loop", "-1",
        "-i", "/opt/mds/stream_inputs/sample1.mp4",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-vf", f"drawtext=fontfile=arial.ttf:text='720p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20,scale=-2:720",
        "-preset", "fast",
        "-map", "0",
        "-f", "flv", f"rtmp://localhost/hls/{output_name}_720",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "128k",
        "-vf", f"drawtext=fontfile=arial.ttf:text='480p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20,scale=-2:480",
        "-preset", "fast",
        "-map", "0",
        "-f", "flv", f"rtmp://localhost/hls/{output_name}_480",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-vf", f"drawtext=fontfile=arial.ttf:text='360p':fontcolor=yellow:fontsize=72:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)-20:y=20,scale=-2:360",
        "-preset", "fast",
        "-map", "0",
        "-f", "flv", f"rtmp://localhost/hls/{output_name}_360",
        "-map", "0:v",
        "-vf", "fps=1/60",
        f"/opt/mds/temp/thumbnails/{output_name}_thumbnail%03d.jpg"
    ]

    # Spuštění procesu
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"FFmpeg spuštěn s PID: {process.pid}")
    return process

# Příklad spuštění s dynamickým názvem
process = run_ffmpeg("test")

# Hlavní program pokračuje
print("Hlavní program pokračuje!")

time.sleep(100)
