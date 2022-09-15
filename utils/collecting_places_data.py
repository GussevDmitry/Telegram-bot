import re

def collecting_data_places(location_info_result):
    places = []
    for i_data in location_info_result.values():
        for j_data in i_data:
            cap_res = j_data.get('caption')
            if cap_res.rfind('span') != -1:
                pre_desc = re.search(r'(?<=span>).+', cap_res[cap_res.rfind('span'):]).group(0).strip()
                if pre_desc.startswith(','):
                    pre_desc = pre_desc[2:]
            else:
                pre_desc = cap_res
            places.append(
                {
                    'dest_ID': j_data.get('destinationId'),
                    'name': j_data.get('name'),
                    'description': pre_desc
                }
            )

    return places
