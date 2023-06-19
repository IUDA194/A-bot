import ffmpeg
import os
import subprocess

class video_update:

    video_path = "video.mp4"
    new_metadata = {"title": "My Modified Video", "artist": "John Doe"}
    user_id = None

    def __init__(self, video_path : str = "video.mp4", metadata : dict = {"title": "My Modified Video", "artist": "John Doe"}, user_id : str = "name") -> None:
        self.video_path = video_path
        self.new_metadata = metadata
        self.user_id = user_id
        self.modify_video_metadata(self.user_id, self.video_path, self.new_metadata)

    def modify_video_metadata(self,user_id, file_path, metadata):
        try:
            command = ['ffmpeg', '-i', file_path]
            for key, value in metadata.items():
                command.extend(['-metadata', f'{key}={value}'])
            command.append(f'{user_id}_r.mp4')
            subprocess.run(command, check=True)
            print('Metadata modified successfully.')
        except subprocess.CalledProcessError as e:
            print(f'Error occurred while modifying metadata: {e}')
            