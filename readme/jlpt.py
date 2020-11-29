# -*- coding: utf-8 -*-

import csv
import logging
import random

from .resources import RESOURCES


LOG = logging.getLogger('jlpt')


def choose_random(level: str = 'n1'):
    LOG.info("Reading %s", RESOURCES / f'jlpt_{level}.csv')
    with open(RESOURCES / f'jlpt_{level}.csv', 'r', encoding='utf-8') as fp:
        data = csv.reader(fp)

        # Ignore the heading
        next(data)

        words = list(data)

        return random.choice(words)
