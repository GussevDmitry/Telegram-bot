import re
import json


def collecting_lm_ids(location_info, data):
    data['querystring_properties_list'].update(
        {'landmarkIds': []}
    )
    pattern_lm = r'(?<="LANDMARK_GROUP",).+?[\]]'
    find_lm = re.search(pattern_lm, location_info)
    if find_lm:
        location_info_result_lm = json.loads(f"{{{find_lm[0]}}}")
        for i_data in location_info_result_lm.get('entities'):
            data['querystring_properties_list']['landmarkIds'].append(
                i_data.get('destinationId')
            )