from src import masks
from src import widget

if __name__ == "__main__":
    print(masks.get_mask_card_number(7000792289606361))
    print(masks.get_mask_account(73654108430135874305))
    print(widget.mask_account_card(
        (
'Maestro 1596837868705199',
'MasterCard 7158300734726758',
'Счет 35383033474447895560',
'Visa Classic 6831982476737658',
'Visa Platinum 8990922113665229',
'Visa Gold 5999414228426353',
        )
    )
)
    print(widget.get_date('2024-03-11T02:26:18.671407'))