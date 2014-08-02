# -*- coding: utf-8 -*-
from plone.recipe.codeanalysis.utils import find_files
from plone.recipe.codeanalysis.utils import log
from sphinxcontrib.spelling.checker import SpellingChecker

import os


def code_analysis_rst_spelling(options):
    log('title', 'rst spelling')

    found_files = find_files(options, '.*\.rst')
    file_paths = set(found_files.strip().split('\n'))
    word_list = os.path.join(os.path.dirname(__file__), 'rst_word_list.txt')

    checker = SpellingChecker(
        lang='en_US',
        suggest=True,
        word_list_filename=word_list,
    )

    all_typos = []
    for file_path in file_paths:
        with open(file_path) as f:
            typos = process_file(f, file_path, checker)
            if typos:
                all_typos += typos  # keep all typos in a flat list

    if len(all_typos) > 0:
        log('failure')
        for typo in all_typos:
            print('{0}:{1} {2} {3}'.format(*typo))
        print('Total errors: {0}'.format(len(all_typos)))
        return False
    else:
        log('ok')
        return True


def process_file(f, file_path, checker):
    typos = []
    for line_number, line_text in enumerate(f):
        if '>>>' in line_text:
            continue
        if '...' in line_text:
            continue
        for word, suggestions in checker.check(line_text):
            typos.append([file_path, line_number + 1, word, suggestions])
    return typos
