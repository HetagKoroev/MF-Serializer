"""Тесты для модуля serializer.py"""


from os import path, stat
import pytest
from serializer import get_file_lines
from serializer import serialize_mf_to_dict
from serializer import get_delimiter_index


META_MANIFEST_MF_LINK = 'MANIFEST.MF'
EMPTY_META_MANIFEST_MF_LINK = 'EMPTY_MANIFEST.MF'
FAKE_FILE = 'DFDF.MF'


def test_check_file_not_found_error():
    """Проверка возбуждения ошибки при отсутствии .mf файла"""
    if not path.isfile(FAKE_FILE):
        with pytest.raises(FileNotFoundError):
            get_file_lines(FAKE_FILE)


def test_check_file_is_empty_error():
    """Проверка возбуждения ошибки при пустом .mf файле"""
    if stat(META_MANIFEST_MF_LINK).st_size < 1:
        with pytest.raises(RuntimeError):
            get_file_lines(META_MANIFEST_MF_LINK)


def test_check_output_one():
    """Проверка вывода(1)"""
    cases = (
             ['Hello: World\n'],
             ['Hello:\nWorld\n'],
             ['Hello: World\n\n'],
             ['Hello:\nWorld\n'],
             ['Hello :\n\nWorld']
             )

    for case in cases:
        assert serialize_mf_to_dict(case, skipped_fields=()) == {'Hello': 'World'}


def test_check_output_two():
    """Проверка вывода(2)"""
    cases = (
            ['Hello: World\n', 'Hi:\nWorld\n'],
            )

    for case in cases:
        assert serialize_mf_to_dict(case, skipped_fields=()) == {'Hello': 'World',
                                                                 'Hi': 'World'}


def test_check_output_three():
    """Проверка вывода(3)"""
    cases = (
            ['Hello: World s\n', ' ome text', 'Hi:\nWorld\n'],
            ['Hello: World s\n', ' ome text', 'Hi:\nWor\n', ' ld\n'],
            ['Hello: World s\n', ' ome t\n', ' ext', 'Hi:\nWor\n', ' ld\n'],
            )

    for case in cases:
        assert serialize_mf_to_dict(case, skipped_fields=()) == {'Hello': 'World some text',
                                                                 'Hi': 'World'}


def test_delimiter_finder():
    """Проверка нахождения индекса разделителя"""
    test_data = (('fhgfhgf:dsfdfdf', 7), ('cbvcv=xc', 5), ('cmvncx,mv', -1))

    for text, indx in test_data:
        assert get_delimiter_index(text) == indx


def test_attributes_excluding():
    """Проверка исключения определенных аттрибутов"""
    test_data = ['hello:111\n', 'hi:222\n', 'good morning: 333\n']
    test_skipp = ('good morning',)

    assert serialize_mf_to_dict(test_data, skipped_fields=test_skipp) == {'hello': '111',
                                                                          'hi': '222'}


def test_skip_comments():
    """Проверка на игнорировение строк комментариев"""
    test_data = ['!hello:000\n', ' .111', 'hi:222\n', '#good morning: 333\n']
    assert serialize_mf_to_dict(test_data) == {'hi': '222'}
