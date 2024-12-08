
# Importing required module
import os
import time

os.system('echo "test python scriptu"')

stream_name1 = input("zadejte klíč streamu1:")
stream_name2 = input("zadejte klíč streamu2:")
stream_name3 = input("zadejte klíč streamu3:")


print("klíč1 je: " + stream_name1)
print("klíč2 je: " + stream_name2)
print("klíč3 je: " + stream_name3)


os.system("touch /opt/mds/temp/tmp_hls/" + stream_name1 + ".m3u8")
time.sleep(0.5)
os.system("touch /opt/mds/temp/tmp_hls/" + stream_name2 + ".m3u8")
time.sleep(0.5)
os.system("touch /opt/mds/temp/tmp_hls/" + stream_name3 + ".m3u8")
