import os


def get_file_path_name_ext(filename: str):
    """
    获取文件路径、文件名、扩展名
    get_extension('6666')
        ('', '6666', '')
    get_extension('6666/jpg')
        ('6666', 'jpg', '')
    get_extension('6666.jpg')
    ('', '6666', '.jpg')
    """
    filepath, tempfilename = os.path.split(filename)
    shotname, extension = os.path.splitext(tempfilename)
    return filepath, shotname, extension
