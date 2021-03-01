from io import BytesIO
import typing
import os

from PIL import Image, ImageFile, ImageOps
from selenium import webdriver

ImageFile.LOAD_TRUNCATED_IMAGES = True


def resize_image(image, width=800, height=800) -> Image.Image:
    """
    修改图片尺寸，如果同时有修改尺寸和大小的需要，可以先修改尺寸，再压缩大小
    :param image: 能够 Image.open() 的对象
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(image)
    out: Image.Image = im.resize((width, height), Image.ANTIALIAS)
    return out


def compress_and_resize_image(image, resize: bool = False, width=800, height=800) -> BytesIO:
    """
    :param image: 能够 Image.open() 的对象
    :param resize: 是否要重置图片大小
    :param width: 指定图片的宽
    :param height: 指定图片的高
    :return: Image.Image
    """
    im: Image.Image = Image.open(image)

    if im.mode != 'RGB':  # png是RGBA的，强转成jpg的RGB，可以大幅减少图片大小
        im = im.convert('RGB')

    if resize:
        im = im.resize((width, height), Image.ANTIALIAS)

    im_io = BytesIO()
    im.save(im_io, format='JPEG', quality=75)
    im_io.seek(0)
    return im_io


def html_file_2_image_content(html_file_abspath) -> bytes:
    """
    :param html_file_path: html文件的绝对路径
    :return: 图片的二进制数据
    """
    driver_get_url = f'file://{html_file_abspath}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    executable_path = os.getenv('CHROMEDRIVER_EXEC_PATH') or 'chromedriver'
    with webdriver.Chrome(executable_path=executable_path, chrome_options=options) as driver:
        driver.set_window_size(4096, 2160)  # 不设置大一点，可能会截图不全
        driver.get(driver_get_url)
        image_content: bytes = driver.get_screenshot_as_png()
        # 基类 WebDriver 实现了 __exit__ 方法，会执行 self.quit()
    return image_content


def crop_image_margin(img_fileobj: typing.Union[BytesIO, str, bytes], padding=(0, 0, 0, 0)) -> bytes:
    """
    裁剪图片的白边
    :param img_fileobj: 泛指一个类文件对象，比如BytesIO就可以
    :param padding: 如果担心检测出来的bbox过小，可以加点padding
    :return: bytes
    """
    with BytesIO(b'') as output_bf:
        if isinstance(img_fileobj, bytes):
            new_img_fileobj = BytesIO()
            new_img_fileobj.write(img_fileobj)
            new_img_fileobj.seek(0)
            img_fileobj = new_img_fileobj
        # 转换成RGB格式，然后运用getbbox方法
        image = Image.open(img_fileobj).convert('RGB')
        # getbbox实际上检测的是黑边，所以要先将image对象反色
        ivt_image = ImageOps.invert(image)
        # 如果担心检测出来的bbox过小，可以加点padding
        bbox = ivt_image.getbbox()
        left = bbox[0] - padding[0]
        top = bbox[1] - padding[1]
        right = bbox[2] + padding[2]
        bottom = bbox[3] + padding[3]
        cropped_image = image.crop([left, top, right, bottom])
        cropped_image.save(output_bf, format='PNG')
        # 取出 bytes 作为返回值，用于保存文件或直接传输都可以
        ret = output_bf.getvalue()
    return ret
