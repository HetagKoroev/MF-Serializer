"""Сериализатор .MF -> Python dict"""


from os import path, stat
from typing import Tuple, List, Dict
from pprint import pprint
from loguru import logger


logger.add('debug.log', format='{time} {level} {message}', level='ERROR')


@logger.catch
def get_delimiter_index(line):
    """Возвращает индекс разделителя"""
    double_dot_index: int = line.find(':')
    compare_op_dot_index: int = line.find('=')
    delimiter_index: int = double_dot_index if compare_op_dot_index == -1 else compare_op_dot_index
    return delimiter_index


@logger.catch
def get_file_lines(file_path: str) -> List[str]:
    """Считать строки из файла и вернуть список строк"""
    if not path.isfile(file_path):
        raise FileNotFoundError(file_path)

    if stat(file_path).st_size < 1:
        raise RuntimeError('Файл пустой.')

    with open(file_path, 'r', encoding='UTF-8') as file:
        all_lines: List[str, ...] = file.readlines()
    return all_lines


@logger.catch
def serialize_mf_to_dict(lines: List[str], skipped_fields='') -> Dict[str, str]:
    """ Принимает список строк и возвращает dict"""
    props_result: Dict[str: str, ...] = {}
    skipped: bool = False
    # Если строка пуста или находится в skipped_fields - пропускаем весь атрибут
    for i, prop_line in enumerate(lines):
        prop_line_stripped = prop_line.strip()
        if (not prop_line_stripped)\
                or (prop_line_stripped[:get_delimiter_index(prop_line_stripped)]
                    in [*skipped_fields]) \
                or (skipped and prop_line.startswith(' '))\
                or any([prop_line_stripped.startswith(ch) for ch in ('!', '#')]):
            skipped = True
            continue

        delimiter_index = get_delimiter_index(prop_line)
        if not prop_line.startswith(' '):
            props_result[prop_line_stripped[:delimiter_index].strip()] =\
                prop_line_stripped[delimiter_index+1:].strip()
        else:
            if skipped:
                continue
            # Перебираем предыдущие строки пока не добрались до ключа атрибута
            while lines[i - 1].startswith(' '):
                i -= 1

            delimiter_index = get_delimiter_index(lines[i - 1])
            props_result[lines[i - 1][:delimiter_index].strip()] += prop_line_stripped
        skipped = False
    return props_result


@logger.catch
def main():
    """Точка входа"""

    meta_manifest_mf_link: str = 'MANIFEST.MF'

    skipped: Tuple[str, ...] = ('exclude this key', )

    all_lines: List[str, ...] = get_file_lines(file_path=meta_manifest_mf_link)
    props: Dict[str: str, ...] = serialize_mf_to_dict(all_lines, skipped)

    pprint(props)


if __name__ == '__main__':
    main()
