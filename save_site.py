from pywebcopy import save_webpage, save_website
import validators
import os
import time
import shutil
import zipfile

class dowobload_site:
    def create_zip_folder(folder_path, output_path):
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

    def webpage(url, folder, name):
        save_webpage(
            url=url,
            project_folder=folder,
            project_name=name,
            bypass_robots=True,
            debug=True,
            open_in_browser=True,
            delay=None,
            threaded=False,
        )

    def website(self, url, folder : str, name, user_id):
        if not os.path.exists(os.path.abspath(folder)): os.mkdir(os.path.abspath(folder))
        try:
                os.rmdir(os.path.abspath(f"{folder}"))
                os.mkdir(os.path.abspath(f"{folder}"))
        except:
                shutil.rmtree(os.path.abspath(f"{folder}"))
                os.mkdir(os.path.abspath(f"{folder}"))
        save_website(
            url=url,
            project_folder=os.path.abspath(folder),
            project_name=name,
            bypass_robots=True,
            debug=True,
            open_in_browser=False,
            delay=None,
            threaded=False)
            

        with zipfile.ZipFile(f"{user_id}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder))
	
        return f"{user_id}.zip"
