# -*- coding: utf-8 -*-

import colorsys
import random
import typing
import math
import logging

from PIL import Image


LOG = logging.getLogger('fractal')


def generate_fractal(
    width: int = 1024, height: int = 1024,
    color: typing.Tuple[float, float, float] = None,
    c: complex = None,
) -> Image.Image:
    im = Image.new('RGB', (width, height), (0, 0, 0))

    color = color or colorsys.hsv_to_rgb(random.random(), 1.0, 1.0)

    c = c or complex(
        (random.random() - 0.5) * 2,
        (random.random() - 0.5) * 2,
    )

    color = tuple(int(x * 255) for x in color)

    # Create fractal mix layer
    LOG.info('Creating fractal mix layer')
    with Image.new('L', (width, height), 0) as mix_layer:
        for y in range(mix_layer.height):
            for x in range(mix_layer.width):
                # Map to coordinate space
                z = complex(
                    ((x / mix_layer.width) - 0.5) * 4,
                    ((y / mix_layer.height) - 0.5) * 4,
                )

                value = 0

                # Calculate fractal
                for iteration in range(100):
                    z = (z ** 2) + c  # Julia fractal

                    if abs(z) > 4:
                        value = ((iteration / 100) * 0.8) + 0.2
                        break

                mix_layer.putpixel((x, y), int(value * 255))
        
        LOG.info('Finished creating fractal mix layer')

        # Mix with color
        with Image.new('RGB', (width, height), color=color) as fill:
            LOG.info('Pasting with mix layer')
            im.paste(fill, (0, 0), mask=mix_layer)

    return im
