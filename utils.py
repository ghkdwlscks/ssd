import re
from constant import NUM_LBA


def can_convert_into_int(_target):
    try:
        int(_target)
    except ValueError:
        return False
    return True


def is_valid_lba(_lda):
    if can_convert_into_int(_lda) and int(_lda) < NUM_LBA:
        return True
    else:
        return False


def is_valid_data(_data):
    import re
    if re.fullmatch(r"0x[0-9A-F]{8}", _data):
        return True
    else:
        return False


def check_nand_txt_read_result_validation(nand_read_result):
    if len(nand_read_result) != NUM_LBA:
        return False
    for _lba, _data in nand_read_result:
        if is_valid_lba(_lba) and is_valid_data(_data):
            continue
        else:
            return False
    return True


def is_ssd_command(command):
    if command in ["help", "exit", "fullread"]:
        return True
    if re.fullmatch(r"read [0-9]{1,2}", command):
        return True
    if re.fullmatch(r"write [0-9]{1,2} 0x[0-9A-F]{8}", command):
        return True
    if re.fullmatch(r"fullwrite 0x[0-9A-F]{8}", command):
        return True
    if re.fullmatch(r"(erase|erase_range) [0-9]{1,2} \b(?:100|\d{1,2})\b$", command):
        return True
    return False