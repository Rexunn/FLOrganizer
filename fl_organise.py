from pathlib import Path
import shutil
#--try optimize (14/08/26)
#Get Target Directory
#-prompt using input wraped in pathlib
#-verify directory exists before proceeding
def dir_finder():
    found = False
    while not found:
        #define fl_dir as a path
        fl_dir = Path(input("Input desired directory: "))
        if (fl_dir).is_dir() == True:
            print ("Directory Found!")
            confirm = input (F'Are you sure {fl_dir} is the right directory? (Y/N)')
            #F string lets you add vars in input, works even tho green
            if confirm and confirm[0].lower() == "y":
                found = True
                print ("Directory Confirmed!")
            else:
                found = False
        else:
            print ("Error: Unable to find Directory")
    return fl_dir

#Scan for FLPs
#-go over flp files only in root directory (non recursive, so binary search??)
def dir_scan(fl_dir):
    print("---Unorganized .flp files found--")
    dir_list = list(fl_dir.glob("*.flp"))
    for flp_file in fl_dir.glob("*.flp"):
        #.name gives name+ file type, .stem gives name wihtout file type
        print(flp_file.name)
    dir_size = len(dir_list) 
     print(f"{dir_size} Files Found")

#Create and Move Project
#-for each file.flp check if directory matching file.stem exists
def mk_dir(fl_dir):
    for flp_file in fl_dir.glob("*.flp"):
        target_folder = fl_dir / flp_file.stem
        if not target_folder.is_dir():
            #- if not create using mkdir and move flp inside
            print(f"{flp_file.stem} Folder not found, Creating missing folder")
            target_folder.mkdir(exist_ok = True) # double check folder doesn't exist b4 making it
            shutil.move(flp_file, target_folder/flp_file.name)
        else:
            print(f"{flp_file.stem} Folder alr exists")

#Move exported audio
#-look for mp3 or wav in root folder, move matching exports into new project folder
def file_move(fl_dir):
    file_types = ("*.mp3", "*.wav")
    for flp_file in fl_dir.glob("*.flp"):
        target_folder = fl_dir / flp_file.stem
        for ext in file_types:
            for audio_file in fl_dir.glob(f"{flp_file.stem}*{ext}"):
                if audio_file.stem == flp_file.stem:
                    print(f"Moving {audio_file.name} to {target_folder}")
                    shutil.move(audio_file, target_folder/audio_file.name)

#Copy Related audio
def copy_audio(fl_dir): # what would i need to feed into this?
#defire path for unsorted quarantine
quarantine = path(fl_dir/"Manual-Review")
#loop through recoridngs + get st_mtime modification time of recordings
#fl_dir.glob("*/*.flp") as it's directly 1 folder in
for audio in fl_dir.glob("*/Audio/*.mp3"):
    #modification time
    mod_time = audio.stat().st_mtime
    matching = []
    #loop through flp files + get st_mtime of flp files
    for flps in fl_dir.glob("*/*.flp"):
        flp_time = flps.stat().st_mtime
        #86400 = 24hrs
        time_diff = abs(mod_time - flp_time)
        if time_diff < 86400:
            matching.append(flps)
    if len(matching) == 1:
        #copy audio to flp folder
        audio_folder = matching[0].parent / "Audio"
        audio_folder.mkdir(exist_ok = True)
        shutil.copy2(audio, audio_folder/audio.name)
    else:
        #move to quarantine
        flp_date_groups = []
        for flp in matching:
            #convert mod time to date string
            #make sub dir in quarantine with date string as name
        print(f"Moving {audio.name} to quarantine")
#how many flps modified
#if 1 make new audio subfolder in flp folder
#if >2 or 0 move to quarantine
#use shutil.copy2() to save metadata
fl_dir = dir_finder()
dir_scan(fl_dir)
mk_dir(fl_dir)
file_move(fl_dir)
#copy_audio(fl_dir)