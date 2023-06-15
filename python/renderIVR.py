"""
we want to convert a directory structure to a dialplan for an IVR for the telefonzelle
 
expected Directory-structure:

import
├── announcement.txt
├── 1-first_sub/
│   ├── announcement.txt
│   ├── 1-first_audio.mp3
│   ├── 2-second_audio.mp3
│   ├── 3-third_audio.mp3
│   └── ...
├── 2-second_sub/
│   ├── announcement.txt
│   ├── 1-first_sub/
│   │   ├── announcement.txt
│   │   ├── 1-first_audio.mp3
│   │   ├── 2-second_audio.mp3
│   │   └── ...
│   └── 2-second_sub
│       ├── announcement.txt
│       ├── 1-first_audio.mp3
│       ├── 2-second_audio.mp3
│       └── ...
├── 3-third_sub/
│   ├── announcement.txt
│   ├── 1-first_sub/
│   │   ├── announcement.txt
│   │   ├── 1-first_audio.mp3
│   │   ├── 2-second_audio.mp3
│   │   └── ...
│   └── 2-second_sub
│       ├── announcement.txt
│       ├── 1-first_audio.mp3
│       ├── 2-second_audio.mp3
│       └── ...
└── ...

for all the levels and sub-level there should be dialplans like this:

[it-1]
; Hauptmenü
exten => s,1,Answer(500)
same => n(start), agi(picotts.agi, "Item 1  Guten Tag", de-DE, any)
;same => n(start), agi(picotts.agi, "Item 1  Guten Tag und Willkommen in der Info-Zelle in Rothenklempenoh. Du kannst hier verschiedene Sachen hören.", de-DE, any)
same => n(eingabe), agi(picotts.agi, " Wähle 1 für Hörspiele oder 2 für was anderes!", de-DE, any)
same => n, WaitExten(15)

exten => 1,1,Goto(it-1.1,s,1)
exten => 2,1,Goto(it-1.2,s,1)
exten => 3,1,Goto(it-1.3,s,1)

exten => e,1,agi(picotts.agi, "Das geht so echt nicht!", de-DE, any)
same => n,Goto(s,eingabe)

[it-1.1]
; Untermenü 2
exten => s,1,Answer(500)
same => n(start), agi(picotts.agi, "Item 1 1 Suche Dir ein Hörspiel aus.", de-DE, any)
same => n(eingabe), agi(picotts.agi, " Wähle 1 für Pumuckel oder 2 für was anderes oder Raute für Zurück!", de-DE, any)
same => n, WaitExten(15)

exten => 1,1,Goto(it-1.1.1,s,1)
exten => 2,1,Goto(it-1.1.2,s,1)
exten => 3,1,Goto(it-1.1.3,s,1)

exten => #,1,Goto(it-1,s,1)

exten => e,1,agi(picotts.agi, "Das geht so nicht!", de-DE, any)
same => n,Goto(it-1.1,s,eingabe)

[it-1.1.1]
; Untermenü 2  1. Wahl
exten => s,1,agi(picotts.agi,"Item 1 1 1 Viel Spass beim Hören. Zum Abbrechen bitte die Raute-Taste drücke.", de-DE, any)
same => n,Background(/var/lib/asterisk/sounds/en/Pumuckl-in-der-Schule, m)
same => n,Goto(it-1.1,s,1)

exten => #,1,agi(picotts.agi,"Du hast die Wiedergabe abgebrochen...", de-DE, any)
same => n,Wait(2)
same => n,Goto(it-1.1,s,1)

[it-1.1.2]
; Untermenü 1  2. Wahl
exten => s,1,agi(picotts.agi,"Item 1 1 2 Was anderes gibt es doch nicht zu hören. Hier geht es nur mit der Raute-Taste zurück", de-DE, any)
same => n,WaitExten(15)
same => n,Goto(it-1.1,s,1)

exten => #,1,agi(picotts.agi,"Du hast die Wiedergabe abgebrochen...", de-DE, any)
same => n,Wait(2)
same => n,Goto(it-1.1,s,1)


[it-1.2]
; Untermenü 2
exten => s,1,Answer(500)
same => n(start), agi(picotts.agi, "Item 1 2 Suche Dir was Anderes aus.", de-DE, any)
same => n(eingabe), agi(picotts.agi, " Wähle 1 für Dieses oder 2 für Jenes oder Raute für Zurück!", de-DE, any)
same => n, WaitExten(15)

exten => 1,1,Goto(it-1.2.1,s,1)
exten => 2,1,Goto(it-1.2.2,s,1)
exten => 3,1,Goto(it-1.2.3,s,1)

exten => #,1,Goto(it-1,s,1)

exten => e,1,agi(picotts.agi, "Das geht so nicht!", de-DE, any)
same => n,Goto(it-1.2,s,eingabe)

[it-1.2.1]
; Untermenü 2  1. Wahl
exten => s,1,agi(picotts.agi,"Item 1 2 1 Dieses! Dieses? Hier gibts nichts zu tun. Hier geht es nur mit der Raute-Taste zurück", de-DE, any)
same => n,WaitExten(15)
same => n,Goto(it-1.2,s,1)

exten => #,1,agi(picotts.agi,"Du hast die Wiedergabe abgebrochen...", de-DE, any)
same => n,Wait(2)
same => n,Goto(it-1.2,s,1)

[it-1.2.2]
; Untermenü 2  2. Wahl
exten => s,1,agi(picotts.agi,"Item 1 2 2 Jenes! Jenes? Hier gibts nichts zu hören. Hier geht es nur mit der Raute-Taste zurück", de-DE, any)
same => n,WaitExten(15)
same => n,Goto(it-1.2,s,1)

exten => #,1,agi(picotts.agi,"Du hast die Wiedergabe abgebrochen...", de-DE, any)
same => n,Wait(2)
same => n,Goto(it-1.2,s,1)


"""

import os
import fnmatch

debug = 0;
convert = 0;

def writeMenuDialplan(f, dirpath):
    f.write("[" + dirpath + "]\n")

    # write start extension
    f.write("exten => s,1,Answer(500)\n")
    f.write('same => n,Set(CHANNEL(hangup_handler_push)=hangup-handler,s,1(args))\n')
    if (debug):
        f.write('same => n(start), agi(picotts.agi, "' + dirpath + '", de-DE, any, any)\n')

    # TODO: check if ansage.txt exists
    try:
        with open(dirpath+'/ansage.txt') as a:
            lines = a.readlines()
            for line in lines:
                f.write('same => n, agi(picotts.agi, "' + line.strip() + '", de-DE, any)\n')
    except FileNotFoundError:
        pass

    # TODO: check if auswahl.txt exists
    try:
        with open(dirpath+'/auswahl.txt') as b:
            lines = b.readlines()
            for line in lines:
                f.write('same => n(auswahl), agi(picotts.agi, "' + line.strip() + '", de-DE, any)\n')
    except FileNotFoundError:
        f.write('same => n(auswahl), agi(picotts.agi, "Hier gibt es keine Wahl. Mit Raute gehts zurück.", de-DE, any)\n')
        pass

    f.write('same => n, WaitExten(15)\n')
    f.write("\n");

    # exception-extension
    f.write('exten => e,1,agi(picotts.agi, "Das geht so echt nicht!", de-DE, any)\n')
    f.write('same => n,Goto(s,auswahl)\n');
    f.write("\n");
    
    # zurück-extension
    f.write('exten => #,1,Goto(' + os.path.split(dirpath)[0] + ',s,1)\n')
    f.write("\n");

    # write forward extensions
    with os.scandir(dirpath) as entries:
        for entry in entries:
            if entry.is_dir():
                f.write('exten => ' + entry.name[0] + ',1,Goto(' + dirpath + '/' + entry.name + ',s,1)\n')
                f.write("\n");
                pass
            if entry.is_file():
                # check for file-type mp3 and maybe other later?
                if fnmatch.fnmatch(entry.name, '*.mp3'):
                    f.write('exten => ' + entry.name[0] + ',1,Goto(' + dirpath + '/' + entry.name + ',s,1)\n')
                    f.write("\n");
                    pass
    f.write('\n')

    #write hangup-handler
    f.write('[hangup-handler]\n')
    f.write('exten => s,1,System(pkill python)\n')
    f.write('same => n,System(pidof mpg123 | xargs kill -9)\n')
    f.write('\n')


def writeAudioDialplan(f, dirpath, filename):
    # convert mp3-file and move to asterisk-folder
    os.system('echo "sox ' + dirpath + '/' + filename + ' -r 8000 -c1 /var/lib/asterisk/sounds/zelle/' + os.path.splitext(filename)[0] + '.gsm"')
    if (convert):
        os.system('sox ' + dirpath + '/' + filename + ' -r 8000 -c1 /var/lib/asterisk/sounds/zelle/' + os.path.splitext(filename)[0] + '.gsm')
    os.system('cp ' + dirpath + '/' + filename + ' /var/lib/asterisk/sounds/zelle/' + filename)

    # generate dialplan for audio

    f.write("[" + dirpath + '/' + filename + "]\n")
    # write start extension
    f.write("exten => s,1,Answer(500)\n")
    f.write('same => n(start),agi(picotts.agi, "Viel Spass beim Hören. Zum Abbrechen bitte die Raute-Taste drücken.", de-DE, any)\n')
    # TODO: different way to kill the fadeIn-script then kill all python...
    f.write('same => n,System(pkill python)\n')
    f.write('same => n,System(python /home/pi/zelle/python/fadeInSound.py &)\n')
    f.write('same => n,System(pidof mpg123 | xargs kill -9)\n')    
    f.write('same => n,System(mpg123 /var/lib/asterisk/sounds/zelle/' + filename + ' &)\n')
    f.write('same => n,Background(/var/lib/asterisk/sounds/zelle/' + os.path.splitext(filename)[0] + ', m)\n')
    f.write('same => n,Goto(' + dirpath + ',s,1)\n')
    f.write('\n')

    # abbruch-extension
    f.write('exten => #,1,agi(picotts.agi,"Du hast die Wiedergabe abgebrochen...", de-DE, any)\n')
    f.write('same => n,System(pidof mpg123 | xargs kill -9)\n')    
    f.write('same => n,Wait(1)\n')
    f.write('same => n,Goto(' + dirpath + ',s,1)\n')
    f.write('\n')
    pass


f = open('extensions_zelle.conf', 'w')

# access the import-directory
for dirpath, dirnames, files in os.walk('../menu'):
    print(f'Found directory: {dirpath}')
    writeMenuDialplan(f, dirpath)
    for filename in files:
        if fnmatch.fnmatch(filename, '*.mp3'):
            writeAudioDialplan(f, dirpath, filename)


f.close()





