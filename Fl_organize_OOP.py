from pathlib import Path
import shutil
import datetime

class FLOrganizer:
    def __init__(self, root_dir):
        #globals
        self.root_dir = Path(root_dir)
        self.projects = {}


    def scan_projects(self):
        #populate self.projects with project names and their paths
        print("==== Scanning For Flp files ====")
        if not self.root_dir.is_dir():
            raise ValueError(f" Error: path {self.root_dir} could not be found")
        else:
            print ("Directory Confirmed!")
        print("---Accessing Projects---")
        dir_list = list(self.root_dir.glob("*.flp"))
        print ("[+] Found: ")
        for flp_file in dir_list:
            print(flp_file.name)
            #store direct path to flp
            self.projects[flp_file.name] = flp_file
        dir_size = len(dir_list)
        print(f"{dir_size} Files Found")

    #make folders for unorganized flps
    def organize_projects(self):
        #create folders + move flp using self.projects
        print(" ==== Moving Projects ====")
        for project_name, project_path in self.projects.items():
            #if project path is same as default folder, create new folder and move flp inside
            target_folder = project_path.parent / Path(project_name).stem
           #try to create folder, if exists, print message and continu
           print(f"Processing: {project_name}")

            if not target_folder.is_dir():
                print(f" [+] Created new folder for {project_name}")
            else: 
                print(f" [-] Folder for {project_name} already exists")

            target_folder.mkdir(exist_ok=True)
            try:
                #update state to new file path
                shutil.move(project_path, target_folder / project_name)
                self.projects[project_name] = target_folder / project_name 
                print(f"[+] Created new directory: {target_folder}")
     #for mp3s not flps       
            except FileNotFoundError:
                print(f"[!] {Path(project_name).stem} Folder already exists, File has already been organized")
                self.projects[project_name] = target_folder / project_name
            except shutil.Error as e:
                print(f"[!] Error moving {project_name}: {e}, file may already exist in target folder")
                self.projects[project_name] = target_folder / project_name
            
    def move_audio(self): #moving finished mp3s/wavs into flp folders
        #use self.projects not glob("*.flp")
        print("=== Moving Mp3s and Wavs ===")
        file_types = ("*.mp3", "*.wav")
        for project_name, project_path in self.projects.items():
            name = Path(project_name).stem
            target_folder = project_path.parent
            for ext in file_types:
                for audio_file in self.root_dir.glob(f"{name}{ext}"):
                    print(f"[+] Match found! Moving {audio_file.name} to {target_folder}")
                    shutil.move(audio_file, target_folder / audio_file.name)
                        
    def copy_audio(self): #moving untitled audios into flp folders or quarantine
        print("==== Sorting Lost Untitled Audio ====")
        #define quaratntine path
        #.mkdir
        quarantine_folder = self.root_dir / "Quarantine"
        quarantine_folder.mkdir(exist_ok=True)

        #loop for loose audio in root dir
        #glob("untitled_*.wav") to get loose audio
        #audio time to date string
        #empty list matching_flps as temp bucket for specific audio file
        
        for audio_files in self.root_dir.glob("untitled_*.wav"):
            print(f"Processing: {audio_files.name}")
            matching_flps = [] #for each audio file
            mod_time = audio_files.stat().st_mtime
            #mod_str = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d") 
        #loop through dictionary
        #get path from dictionary value
        #get st mttime 
            for project_name, project_path in self.projects.items():
                flp_time = project_path.stat().st_mtime
                #flp_str = datetime.datetime.fromtimestamp(flp_time).strftime("%Y-%m-%d")
                
                if abs(mod_time - flp_time) < 86400: # 24 hours in seconds
                    print(f"[+] Match found for {audio_files.name}")
                    matching_flps.append(project_path) #add matching flp to list
        #>1 match, put both files in quarantine
            if len(matching_flps) == 1:
                #copy audio to flp folder
                audio_folder = matching_flps[0].parent / "Audio"
                audio_folder.mkdir(exist_ok=True)
                shutil.copy2(audio_files, audio_folder / audio_files.name)      
            else:
                print(f"[!] Multiple matches found for {audio_files.name}. Moving to quarantine.")
                shutil.copy2(audio_files, quarantine_folder / audio_files.name)
    def run(self):
        self.scan_projects()
        self.organize_projects()
        self.move_audio()
        self.copy_audio()

#is script run directly, not imported
if __name__ == "__main__":
    root_dir = input("Enter the path to the root directory: ")
    organizer = FLOrganizer(root_dir)
    organizer.run()