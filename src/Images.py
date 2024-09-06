import imgkit
import os


def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

        
def generate_image_from_html(html_template):
    print(html_template)
    base_path = os.path.abspath(os.path.dirname('public'))
    folder_path = os.path.join(base_path, 'public' ,'img', 'web')
    ensure_directory_exists(folder_path)
    save_path = folder_path + '\\' + 'fear_greed_index.png'

    imgkit.from_string(html_template, save_path)
