# -*- coding: utf-8 -*-

import datetime
import logging
import logging.handlers
import pathlib
import sys

from dateutil import relativedelta, tz
from dateutil.tz import UTC

from readme import fractal, jlpt, now
from readme.templates import get_template


OUTPUT_RESOURCES = pathlib.Path('generated')
OUTPUT_LICENSE = pathlib.Path('LICENSE')
OUTPUT_README = pathlib.Path('README.md')

UTC_NOW = datetime.datetime.utcnow().replace(tzinfo=tz.UTC)


LOGGER: logging.Logger = logging.getLogger()
LOGGER.setLevel(logging.INFO)

LOG_FORMAT: logging.Formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
LOG_STREAM: logging.Handler = logging.StreamHandler(stream=sys.stdout)

LOG_STREAM.setFormatter(LOG_FORMAT)

LOGGER.addHandler(LOG_STREAM)


LOG = logging.getLogger('generate')


# Generate now.png
LOG.info('Generating %s', OUTPUT_RESOURCES / 'now.png')
with open(OUTPUT_RESOURCES / 'now.png', 'wb') as output:
    with now.generate(UTC_NOW) as im:
        im.save(output, format='png')

# Generate fractal
LOG.info('Generating %s', OUTPUT_RESOURCES / 'fractal.png')
with open(OUTPUT_RESOURCES / 'fractal.png', 'wb') as output:
    with fractal.generate_fractal() as im:
        im.save(output, format='png')

# Get JLPT words
LOG.info('Getting JLPT vocabulary')
jlpt_words = {
    'N1': jlpt.choose_random('n1'),
    'N2': jlpt.choose_random('n2'),
    'N3': jlpt.choose_random('n3'),
    'N4': jlpt.choose_random('n4'),
    'N5': jlpt.choose_random('n5'),
}

# Generate LICENSE
LOG.info('Generating %s', OUTPUT_LICENSE)
with open(OUTPUT_LICENSE, 'w', encoding='utf-8') as output:
    output.write(get_template('LICENSE').render(
        now=UTC_NOW,
    ))

# Generate README.md
LOG.info('Generating %s', OUTPUT_README)
with open(OUTPUT_README, 'w', encoding='utf-8') as output:

    # Hour for world clock
    hour = UTC_NOW.hour % 12
    if hour == 0:
        hour = 12

    hour_emoji = chr(0x1F54F + hour)

    # Year percentage bar
    current_year = UTC_NOW.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    next_year = current_year.replace(year=current_year.year + 1)

    current_seconds = (UTC_NOW - current_year).total_seconds()
    total_seconds = (next_year - current_year).total_seconds()

    year_percentage = (current_seconds / total_seconds)
    filled_blocks = int(year_percentage * 20)
    
    percentage_bar = ''.join((['\N{FULL BLOCK}'] * filled_blocks) + (['\N{LOWER ONE EIGHTH BLOCK}'] * (20 - filled_blocks)))

    output.write(get_template('README.md').render(
        hour_emoji=hour_emoji,
        jlpt_words=jlpt_words,
        now=UTC_NOW,
        percentage_bar=percentage_bar,
        year_percentage=year_percentage,
    ))
