
# MDS projct

Aplikace na dynamické vyvtáření streamů.


# Nástroje

+ Debian 12
+ Nginx with RTMP module
+ OBS
+ Python
+ Web browser
+ text editor

# Setup
1. **Příprava prostředí**

Ujistěte se, že všechny potřebné soubory jsou připraveny ve složce `/opt/mds/scripts/`:

+ `enabled_keys.py` – obsahuje seznam povolených klíčů (každý klíč na samostatném řádku).

+ `online_keys.py` – musí být prázdný soubor.

+ `streams.py` – musí být prázdný soubor.

Upravte `/etc/nginx/nginx.conf`, dle připraveného souboru `nginx.conf`.

Do adresáře `/usr/share/nginx/html` vložte `index.html` a `generateCards.js`.

Musí existovat adresář `/opt/mds/stream_inputs` se soubory `sample1.mp4`, `sample2.mp4`,..., `sample4.mp4`, ze kterých se budou generovat streamy.

2. **Spuštění kontrolního skriptu**

Spusťte soubor `key_checker3.py`. Tento skript bude naslouchat změnám v systému a zajišťovat, že každá změna bude registrována.

3. **Vytvoření zdrojového streamu**

Spusťte OBS (Open Broadcaster Software) nebo soubor `creator.py`. Tento krok detekuje změnu a provede autorizaci a případně spustí hls streamy.

4. **Nastavení v OBS**
Při vytváření streamu si vyberete jaký z nabízených možností si přejete zobrazovat. Možnosti jsou mezi Řečník (stream zobrazuje pouze kameru přednášejícího) Řečník+slidy (vaše kamera se nachází v pravém dolním rohu a hlavní zaměření streamu je přenášené slidy) s Slidy (tento stream přenáší pouze Vámi požadované streamy bez vaší kamery).

5. **Běh systému**

Během běhu systému sleduje key_checker3.py změny v souborech. Když je stream ukončen (vypnete OBS nebo ukončíte `creator.py`), vše se automaticky ukončí.



