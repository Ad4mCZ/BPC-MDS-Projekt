
# Importing required module
import os
import time
import threading
import subprocess

os.system('echo "test python scriptu"')

stream_name1 = input("zadejte klíč streamu1:")
stream_name2 = input("zadejte klíč streamu2:")
stream_name3 = input("zadejte klíč streamu3:")


print("klíč1 je: " + stream_name1)
print("klíč2 je: " + stream_name2)
print("klíč3 je: " + stream_name3)


#os.system("ffmpeg -re -i /opt/mds/stream_inputs/sample2.mp4 -c copy -f flv rtmp://127.0.0.1/input/" + stream_name1)
#time.sleep(0.5)
#os.system("ffmpeg -re -i /opt/mds/stream_inputs/sample3.mp4 -c copy -f flv rtmp://127.0.0.1/input/" + stream_name2)
#time.sleep(0.5)
#os.system("ffmpeg -re -i /opt/mds/stream_inputs/sample4.mp4 -c copy -f flv rtmp://127.0.0.1/input/" + stream_name3)


def run_ffmpeg(input_name, output_name):

    input_base_path = "/opt/mds/stream_inputs/"
    output_base_url = "rtmp://127.0.0.1/input/"
    
    # Sestavení úplných cest
    input_file = input_base_path + input_name
    output_url = output_base_url + output_name

    # Definice příkazu FFmpeg s dynamickým názvem výstupu

    command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",  # Nekonečné opakování vstupního souboru
        "-i", input_file,
        "-c", "copy",
        "-f", "flv",
        output_url
    ]
    # Spuštění procesu
    #os.system(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"FFmpeg spuštěn s PID: {process.pid}")
    print(command)
    return process
#os.system(command)
run_ffmpeg("sample2.mp4", stream_name1)
run_ffmpeg("sample3.mp4", stream_name2)
run_ffmpeg("sample4.mp4", stream_name3)


time.sleep(5000)
