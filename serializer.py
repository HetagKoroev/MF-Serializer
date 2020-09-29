from os import path, stat
from typing import Tuple, List, Dict
from pprint import pprint
from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', level='ERROR')


META_MANIFEST_MF_LINK: str = 'MANIFEST.MF'


@logger.catch
def get_delimiter_index(line):
    double_dot_index: int = line.find(':')
    compare_op_dot_index: int = line.find('=')
    delimiter_index: int = double_dot_index if compare_op_dot_index == -1 else compare_op_dot_index
    return delimiter_index


@logger.catch
def get_file_lines(file_path: str) -> List[str]:
    if not path.isfile(META_MANIFEST_MF_LINK):
        raise FileNotFoundError(META_MANIFEST_MF_LINK)
    elif stat(META_MANIFEST_MF_LINK).st_size < 1:
        raise RuntimeError('Файл пустой.')

    with open(file_path, 'r', encoding='UTF-8') as f:
        all_lines: List[str, ...] = f.readlines()
    return all_lines


@logger.catch
def serialize_mf_to_dict(lines: List[str], skipped_fields='') -> Dict[str, str]:
    """ Сериализатор: .mf -> dict object. """
    props_result: Dict[str: str, ...] = {}
    skipped: bool = False
    # Если строка пуста или находится в skipped_fields - пропускаем весь атрибут.
    for i, prop_line in enumerate(lines):
        prop_line_stripped = prop_line.strip()
        if (not prop_line_stripped) or (prop_line_stripped[:get_delimiter_index(prop_line_stripped)] in [*skipped_fields]) \
                or (skipped and prop_line.startswith(' ')) or any([prop_line_stripped.startswith(ch) for ch in ('!', '#')]):
            skipped = True
            continue

        delimiter_index = get_delimiter_index(prop_line)
        if not prop_line.startswith(' '):
            props_result[prop_line_stripped[:delimiter_index].strip()] = prop_line_stripped[delimiter_index+1:].strip()
        else:
            if skipped:
                continue
            # Перебираем предыдущие строки пока не добрались до ключа атрибута.
            while lines[i - 1].startswith(' '):
                i -= 1

            delimiter_index = get_delimiter_index(lines[i - 1])
            props_result[lines[i - 1][:delimiter_index].strip()] += prop_line_stripped
        skipped = False
    return props_result


@logger.catch
def main():
    skipped: Tuple[str, ...] = ('exclude this key', )

    all_lines: List[str, ...] = get_file_lines(file_path=META_MANIFEST_MF_LINK)
    props: Dict[str: str, ...] = serialize_mf_to_dict(all_lines, skipped)

    pprint(props)


if __name__ == '__main__':
    main()
