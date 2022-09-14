import re


def get_correct_price(i_item_dict):
    patterns = [r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}', r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}',
                r'\d{1,}[,.]+?\d{1,}', r'\d{1,}']
    pattern_cur = r'[RUE]\w{2}'
    res_cur = re.search(pattern_cur, i_item_dict.get('ratePlan').get('price').get('fullyBundledPricePerStay'))
    for i_pat in patterns:
        res_pr = re.search(i_pat, i_item_dict.get('ratePlan').get('price').get('fullyBundledPricePerStay'))
        if res_pr:
            return f"{res_pr.group(0)} {res_cur.group(0)}"