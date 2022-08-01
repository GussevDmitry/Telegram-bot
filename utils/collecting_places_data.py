import re

def collecting_data_places(location_info_result):
    places = []
    for i_data in location_info_result.values():
        for j_data in i_data:
            places.append(
                {
                    'dest_ID': j_data.get('destinationId'),
                    'name': j_data.get('name'),
                    'description': re.search(r'(?<=span>, ).+', j_data.get('caption')).group(0).strip()
                }
            )

    return places