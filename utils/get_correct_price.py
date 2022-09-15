import re


def get_correct_price(i_item_dict):
    patterns = [r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}', r'\d{1,}[,.]+?\d{1,}[,.]+?\d{1,}',
                r'\d{1,}[,.]+?\d{1,}', r'\d{1,}']
    for i_pat in patterns:
        res_pr = re.search(i_pat, i_item_dict.get('ratePlan').get('price').get('fullyBundledPricePerStay'))
        if res_pr:
            return f"{res_pr.group(0)}"