from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(confidential_info: tuple) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    to_mask_info = []
    info_name = []
    result = []
    result_str = []
    for info_item in confidential_info:
        splitting_info_item = info_item.split()
        for part in splitting_info_item:
            if part.isdigit():
                to_mask_info.append(part)
            elif part.isalpha():
                info_name.append(' '.join(splitting_info_item[:-1]))
    for el in to_mask_info:
        if len(el) == 16:
            result.append(get_mask_card_number(int(el)))
        elif len(el) == 20:
            result.append(get_mask_account(int(el)))
    for i in range(len(result)):
        result_str.append(f"{info_name[i]} {result[i]}")
    return "\n".join(result_str)
