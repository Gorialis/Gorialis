# -*- coding: utf-8 -*-

import collections
import colorsys
import datetime
import logging
import math

from dateutil import relativedelta, tz
from PIL import Image, ImageDraw, ImageFont

from .resources import RESOURCES

NOW = RESOURCES / 'now'
LOG = logging.getLogger('now')
TIMEZONES = (
    # (name, tz)
    ("Auckland",            tz.gettz("Pacific/Auckland")),
    ("Berlin",              tz.gettz("Europe/Berlin")),
    ("Brisbane",            tz.gettz("Australia/Brisbane")),
    ("Chicago",             tz.gettz("America/Chicago")),
    ("Denver",              tz.gettz("America/Denver")),
    ("L.A.",                tz.gettz("America/Los_Angeles")),
    ("London",              tz.gettz("Europe/London")),
    ("Moscow",              tz.gettz("Europe/Moscow")),
    ("New York",            tz.gettz("America/New_York")),
    ("Paris",               tz.gettz("Europe/Paris")),
    ("Perth",               tz.gettz("Australia/Perth")),
    ("Seoul",               tz.gettz("Asia/Seoul")),
    ("Shanghai",            tz.gettz("Asia/Shanghai")),
    ("Tokyo",               tz.gettz("Asia/Tokyo")),
    ("Urumqi",              tz.gettz("Asia/Urumqi")),
)


def create_color_circle(size: int) -> Image.Image:
    # This function is the slow way to generate the color circle used to tint the globe image.
    # In the actual function, a cached version is loaded instead
    LOG.info('Generating color circle of size %dx%d', size, size)

    im = Image.new('RGB', (size, size), color=(0, 0, 0))

    for y in range(im.height):
        for x in range(im.width):
            # Get radius at this point
            radius = math.sqrt(
                pow(x - (im.width / 2), 2) +
                pow(y - (im.height / 2), 2)
            )

            radius /= size

            radius = min(radius, 0.5) * 2

            # Get angle at this point
            angle = math.atan2(
                (im.width / 2) - x,
                y - (im.height / 2),
            ) / (2 * math.pi)

            # Center to hour
            angle -= (0.5 / 12)

            if angle < 0.0:
                angle += 1.0

            radius = pow(radius, 3)

            r, g, b = colorsys.hsv_to_rgb(angle, radius, 0.5 + (radius / 2))
            r, g, b = (int(x * 255) for x in (r, g, b))

            im.putpixel((x, y), (r, g, b))

    return im


def generate(time: datetime.datetime) -> Image.Image:
    LOG.info('Loading outer ring')
    with Image.open(NOW / 'outer_ring.png') as outer_ring:
        outer_ring = outer_ring.convert('RGBA')

        utc = time.astimezone(tz.UTC)

        # Paste the globe in the middle
        LOG.info('Loading globe')
        with Image.open(NOW / 'globe.png') as globe:
            globe = globe.convert('RGBA')

            # Rotate by hours
            globe = globe.rotate(-15 * (utc.hour - 11.5))

            # Load the cached color circle
            # To do the slow but cacheless method, replace this with:
            #   with create_color_circle(globe.width) as color_circle:
            LOG.info('Loading color circle')
            with Image.open(NOW / 'color_circle.png') as color_circle:
                color_circle = color_circle.convert('RGB').resize(globe.size, Image.BICUBIC)

                # Paste in middle
                LOG.info('Pasting globe')
                outer_ring.paste(color_circle, (
                    round((outer_ring.width - globe.width) / 2),
                    round((outer_ring.height - globe.height) / 2),
                ), mask=globe)

        # Collect up timezones
        LOG.info('Aggregating timezones')
        timezones = collections.defaultdict(list)

        for name, timezone in TIMEZONES:
            local_time = time.astimezone(timezone)
            timezones[local_time.hour].append(name)

        # Load font
        LOG.info('Loading font')
        font = ImageFont.truetype(str(RESOURCES / 'NotoSans-Bold.ttf'), 48)

        # Create text for each timezone segment
        for hour, timezones in timezones.items():
            LOG.info('Drawing hour %d', hour)
            with Image.new("RGBA", outer_ring.size, (0, 0, 0, 0)) as im:
                draw = ImageDraw.Draw(im)

                # Draw each timezone for this hour
                for offset, timezone in enumerate(timezones):
                    offset_y = (offset * font.size * 1.2) + int(im.height * 0.075)
                    offset_x = round(im.width / 2)

                    r, g, b = colorsys.hsv_to_rgb(hour / 24, 1.0, 1.0)
                    r, g, b = (int(x * 255) for x in (r, g, b))

                    draw.text(
                        (offset_x, offset_y),
                        text=timezone,
                        fill=(r, g, b, 255),
                        font=font,
                        anchor="ms",
                    )

                # Rotate by hour
                im = im.rotate(-15 * (hour - 11.5))

                # Paste in middle
                LOG.info('Pasting hour %d', hour)
                outer_ring.paste(im, (
                    round((outer_ring.width - im.width) / 2),
                    round((outer_ring.height - im.height) / 2),
                ), mask=im)

        # Return a copy to make sure the original file is closed
        LOG.info('Resizing output')
        return outer_ring.resize((1024, 1024), Image.BICUBIC)
