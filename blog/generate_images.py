import os
import pathlib
from typing import Tuple

from PIL import Image, ImageDraw


PATH = pathlib.Path(__file__).parent.absolute()


COLOR_MAP = {
    # Light Blue
    0: (9, 178, 246),
    # Light Pink
    1: (255, 110, 216),
    # Verminon Red
    2: (214, 70, 70),
    # Sheen Green
    3: (123, 214, 71),
    # Straw
    4: (234, 221, 105),
    # Mango Tango
    5: (255, 143, 78),
    # Aquamarine
    6: (128, 255, 185),
    # Medium Purple
    7: (140, 128, 255),
    # Mindaro (kind of yellow green)
    8: (206, 255, 128),
    # Medium Slate Blue
    9: (128, 132, 255),
    # SPECIAL CASE: WHITE
    'white': (255, 255, 255)
}

RECTANGLE_CONSTRUCTOR_MAP = {
    0: lambda x, y: (x * 0.4, y * 0.3, x * 0.9, y * 0.8),
    1: lambda x, y: (x * 0.4, y * 0.3, x * 0.9, y * 0.7),
    2: lambda x, y: (x * 0.2, y * 0.4, x * 0.6, y * 0.7),
    3: lambda x, y: (x * 0.3, y * 0.3, x * 0.6, y * 0.8),
    4: lambda x, y: (x * 0.4, y * 0.3, x * 0.8, y * 0.6),
    5: lambda x, y: (x * 0.4, y * 0.2, x * 0.9, y * 0.4),
    6: lambda x, y: (x * 0.1, y * 0.4, x * 0.7, y * 0.6),
    7: lambda x, y: (x * 0.1, y * 0.1, x * 0.4, y * 0.4),
    8: lambda x, y: (x * 0.2, y * 0.3, x * 0.6, y * 0.7),
    9: lambda x, y: (x * 0.1, y * 0.1, x * 0.5, y * 0.4),
}


def generate_geometric_image(hash_id: int,
                             image_size: Tuple[int, int] = (100, 100)) -> Image:

    # "hash_id" will be a decimal integer number with three places (or at least for the purposes of this method only
    # the three last places will be relevant). Each of these three digits controls one aspect of the generation process
    # In general, the images are supposed to be a composition of very geometric shapes of varying colors and positions.

    # Here we separate the three last digits. I am sure there are better ways to do this with shifting and what not,
    # but this string method works and is simple to implement
    hash_id_string = str(hash_id)
    background_color_key = int(hash_id_string[-1])
    foreground_color_key = int(hash_id_string[-2])
    position_key = int(hash_id_string[-3])

    # It kind of looks weird when the foreground and background color are the same, which is why when this would be the
    # case we instead set the foreground color to the special color "white"
    if background_color_key == foreground_color_key:
        foreground_color_key = 'white'

    im = Image.new('RGB', image_size, COLOR_MAP[background_color_key])
    draw = ImageDraw.Draw(im)

    rectangle_constructor = RECTANGLE_CONSTRUCTOR_MAP[position_key]
    draw.rectangle(rectangle_constructor(*image_size), fill=COLOR_MAP[foreground_color_key], outline=(0, 0, 0))

    return im


def generate_random_rectangle_map():
    import random
    for i in range(10):
        x_start = random.randrange(1, 5, 1) / 10
        x_width = random.randrange(3, 7, 1) / 10
        x_end = round(x_start + x_width, 1)

        y_start = random.randrange(1, 5, 1) / 10
        y_width = random.randrange(2, 6, 1) / 10
        y_end = round(y_start + y_width, 1)

        print(f'{i}: lambda x, y: (x * {x_start}, y * {y_start}, x * {x_end}, y * {y_end}),')


if __name__ == '__main__':

    static_path = os.path.join(PATH, 'static')
    images_path = os.path.join(static_path, 'comment_images')

    for i in range(1000):
        hash_id = 1000 + i
        image_name = f'{i:03d}.jpg'
        image_path = os.path.join(images_path, image_name)
        im = generate_geometric_image(hash_id)
        im.save(image_path, quality=95)

        print(f'Saved {image_name}')
