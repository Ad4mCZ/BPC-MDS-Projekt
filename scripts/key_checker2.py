import time
import sys
import os
import threading
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def file_reader(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            values = {row.strip() for row in f if row.strip()}
        return values
    except FileNotFoundError:
        print(f"Soubor '{file}' nebyl nalezen.")
        return set()

def eval_key(zadany_klic, povoleny_klic, aktivni_klic):
    if zadany_klic in povoleny_klic and zadany_klic not in aktivni_klic:
        print("stream povolen")
        return 1
    elif zadany_klic in povoleny_klic:
        print("Hodnota je povolená, ale je již používána")
        return 2
    else:
        print("Hodnota není povolena")
        return 0

def file_append(file, key):

    try:
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"{key}\n")
        #print(f"Stream '{key}' je nyní aktivní")
    except Exception as e:
        print(f"Chyba při přidávání hodnoty do souboru: {e}")

#self.detected_names = set()

class NewFolderHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
        self.detected_name = None
        self.event_type = None
        #self.detected_names = set()

    def process_file(self, path, streams):
        """
        Zpracuje cestu k souboru a uloží část názvu souboru, pokud je nová.
        """
        file_name = os.path.basename(path)
        # Najdi část názvu před pomlčkou nebo podtržítkem
        base_name = file_name.split('-')[0].split('_')[0].split('.')[0]
        print("kuk")
        if base_name not in streams: #tu se musí checkovat soubor
            file_append("streams.txt", base_name)
            #self.detected_names.add(base_name)
            print(f"Nový soubor nalezen: {path}")
            print(f"Detekován nový stream: {base_name}")
            self.detected_name = base_name
        #else:
           # print(f"Název {base_name} již byl detekován.")
           # self.detected_name = None
        return


    def on_created(self, event):
         streams = file_reader("streams.txt")
         self.process_file(event.src_path, streams)
#        time.sleep(0.1)
#        if event.is_directory:
#            pass
#        elif event.src_path.endswith('.m3u8'):
#            print(f"Nový soubor nalezen: {event.src_path}")
#            print(f"Nový stream: {os.path.splitext(os.path.basename(event.src_path))[0]}")
#            self.detected_name = os.path.splitext(os.path.basename(event.src_path))[0]
#            new_folder = 1
            #print(new_folder)
         self.event_type = 'created'
         self.observer.stop()
           # return event.src_path

#    def on_deleted(self, event):
#        if event.is_directory:
#            pass
#        elif event.src_path.endswith('.m3u8'):
#            print(f"Odstranen soubor: {event.src_path}")
#            print(f"Zrušený stream: {os.path.splitext(os.path.basename(event.src_path))[0]}")
#            self.detected_name = os.path.splitext(os.path.basename(event.src_path))[0]
#            self.event_type = 'deleted'
#            self.observer.stop()

    def get_aktivni_streamy(self):
        if not os.path.exists("streams.txt"):
            return set()

        with open("streams.txt", "r") as f:
            return set(line.strip() for line in f.readlines() if line.strip())
 #       return

    def kontroluj_streamy(self, monitored_dir):
        aktivni_streamy = self.get_aktivni_streamy()
        existujici_soubory = {os.path.splitext(f)[0] for f in os.listdir(monitored_dir) if f.endswith('.m3u8') and "-" not in f and "_" not in f and not(f.endswith('.m3u8.bak'))}
        #print(existujici_soubory)
        # Najdi aktivní streamy, které již neexistují
        self.chybejici_soubory = aktivni_streamy - existujici_soubory
        #print(f"neaktivni streamy: {self.chybejici_soubory}")
        return self.chybejici_soubory

    def on_deleted(self, event):
        time.sleep(0.1)
        monitored_dir = os.path.dirname(event.src_path)
        zjisteny_stream = self.kontroluj_streamy(monitored_dir)
#        time.sleep(5)
#        zjisteny_stream2 = self.kontroluj_streamy(monitored_dir)
#        if zjisteny_stream != zjisteny_stream2:
#            print("nesrovnalost")
#            return
        #print(', '.join(zjisteny_stream))
        if zjisteny_stream:
            print(f"Chybějící streamy: {', '.join(zjisteny_stream)}")
#        else:
#            print("odstranuji.")
            self.detected_name = zjisteny_stream
            self.event_type = 'deleted'
            self.observer.stop()
        return



def row_remover(file, value):
    if file and value:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            # Odstranění řádku odpovídajícího názvu
            with open(file, 'w') as f:
                for line in lines:
                    if line.strip() != value:
                        f.write(line)

            print(f"'{value}' bylo odstraněno ze souboru '{file}'.")
        except FileNotFoundError:
            print(f"Soubor '{file}' nebyl nalezen.")
        except Exception as e:
            print(f"Chyba při úpravě souboru '{file}': {e}")


def observer_folder(folder):
    if not os.path.exists(folder):
        print(f"Složka '{folder}' neexistuje.")
        return

    observer = Observer()
    handler = NewFolderHandler(observer)
    observer.schedule(handler, folder, recursive=False)
    print("-----------------------------------------")
    print(f"Sleduji složku: {folder}")
    try:
        print("čekám na změny...")
        observer.start()
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("\nSledování ukončeno.")
    observer.join()
    return handler.detected_name, handler.event_type


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



#---------------------------main----------------------------
povoleny_klic = file_reader("enabled_keys.txt")
aktivni_klic = file_reader("online_keys.txt")
#streams = file_reader("streams.txt")

mode = "initial"

while True:
        new_folder = 0
#	mode = input("Pro pokračování stistněte ENTER, nebo zadejte exit pro ukončení:").strip()
#	if mode == "exit":
#		sys.exit()
        zjisteny_stream, typ_zmeny = observer_folder("/opt/mds/temp/tmp_hls")
	#print(zjisteny_stream)

        if zjisteny_stream and typ_zmeny:
            print(f"Zachycena událost: {typ_zmeny}. Objekt: {zjisteny_stream}")
            notification = "'MDS Python script' 'Stream: " + zjisteny_stream + " byl: " + typ_zmeny + "'"
           # os.system("notify-send " + notification)
            evaluation = eval_key(zjisteny_stream, povoleny_klic, aktivni_klic)
            print(f"evaluaiton: {evaluation}")
            if typ_zmeny == "created":
#                print("detekovan typ created")
                #evaluation = eval_key(zjisteny_stream, povoleny_klic, aktivni_klic)
                if evaluation == 1:
                        print(f"spouštění vysílání a zápis mezi aktivní: {zjisteny_stream}")
                        file_append("online_keys.txt", zjisteny_stream)
                        #exec
                        #ffmpeg_script(zjisteny_stream)
                        process = run_ffmpeg(zjisteny_stream)

            elif typ_zmeny == "deleted" and evaluation == 2:
                print("bylo vypnuto vysílání a je odstraněno z aktivních")
                for stream in zjisteny_stream:
                     row_remover("online_keys.txt", stream)
                     row_remover("streams.txt", stream)

            elif typ_zmeny == "deleted":
                print("zavolana funkce pro odstranění, ale chyba")
                for stream in zjisteny_stream:
                     row_remover("streams.txt", stream)
                     row_remover("online_keys.txt", stream)

        else:
            print("Script běží, streamy běží")


#	zadany_klic = input("Zadejte streamovací klíč: ").strip()
                #exec

        time.sleep(1)

