import time
import sys
import os
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
        print("Stream '{key}' je nyní aktivní")
    except Exception as e:
        print(f"Chyba při přidávání hodnoty do souboru: {e}")


class NewFolderHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
        self.detected_name = None
        self.event_type = None

    def on_created(self, event):
#        time.sleep(0.1)
        if event.is_directory:
            pass
        elif event.src_path.endswith('.m3u8'):
            print(f"Nový soubor nalezen: {event.src_path}")
            print(f"Nový stream: {os.path.splitext(os.path.basename(event.src_path))[0]}")
            self.detected_name = os.path.splitext(os.path.basename(event.src_path))[0]
            new_folder = 1
            #print(new_folder)
            self.event_type = 'created'
            self.observer.stop()
           # return event.src_path

    def on_deleted(self, event):
        if event.is_directory:
            pass
        elif event.src_path.endswith('.m3u8'):
            print(f"Odstranen soubor: {event.src_path}")
            print(f"Zrušený stream: {os.path.splitext(os.path.basename(event.src_path))[0]}")
            self.detected_name = os.path.splitext(os.path.basename(event.src_path))[0]
            self.event_type = 'deleted'
            self.observer.stop()

def key_remover(file, value):
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


#---------------------------main----------------------------
povoleny_klic = file_reader("enabled_keys.txt")
aktivni_klic = file_reader("online_keys.txt")

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
            evaluation = eval_key(zjisteny_stream, povoleny_klic, aktivni_klic)
            if typ_zmeny == "created":
#                print("detekovan typ created")
                #evaluation = eval_key(zjisteny_stream, povoleny_klic, aktivni_klic)
                if evaluation == 1:
                        print(f"spouštění vysílání: {zjisteny_stream}")
                        file_append("online_keys.txt", zjisteny_stream)
                        #exec

            elif typ_zmeny == "deleted" and evaluation == 1:
                print("bylo vypnuto vysílání a je odstraněno z aktivních")
                key_remover("online_keys.txt", zjisteny_stream)

        else:
            print("Nebyla zachycena žádná událost.")


#	zadany_klic = input("Zadejte streamovací klíč: ").strip()
                #exec

        time.sleep(10)

