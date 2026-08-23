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
def copy_audio(): # what would i need to feed into this?

fl_dir = dir_finder()
dir_scan(fl_dir)
mk_dir(fl_dir)
file_move(fl_dir)
