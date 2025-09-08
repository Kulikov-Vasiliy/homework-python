import logging

logger = logging.getLogger("masks")
file_handler = logging.FileHandler("logs/masks.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    if not card_number.isdigit():
        logger.info("проверка номера карты на целочисленность")
        raise TypeError("некорректный тип данных")

    if len(card_number) != 16:
        logger.info("Проверка длины номера карты")
        raise ValueError(
            "номер карты должен состоять из 16 символов или нет открытых продуктов"
        )

    first_num = card_number[0:4]
    middle_num = card_number[4:6]
    last_num = card_number[-4:]
    logger.info("Маскируется номер карты")

    logger.info("Возвращается замаскированный номер карты")
    return f"{first_num} {middle_num}** **** {last_num}"


def get_mask_account(client_account: str) -> str:
    """Функция маскировки номера банковского счета"""
    if not client_account.isdigit():
        logger.info("проверка номера счета на целочисленность")
        raise TypeError("некорректный тип данных или нет открытых счетов")

    if len(client_account) != 20:
        logger.info("Проверка длины номера счета")
        raise ValueError("банковский счет должен состоять из 20 символов")

    late_num = client_account[-4:]
    logger.info("Маскируется номер счета")

    logger.info("Возвращается замаскированный номер счета")
    return f"**{late_num}"
