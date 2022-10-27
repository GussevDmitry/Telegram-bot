import re
import json
from typing import List


def collecting_data_places(location_info_result: json) -> List:
    """
    Collecting the information about found places
    :param location_info_result: json file containing the information about city groups
    :return: the list with the information about found places
    """
    places = []
    for i_data in location_info_result.values():
        for j_data in i_data:
            cap_res = j_data.get('caption')
            desc_before_span = cap_res[:cap_res.find("<span")]
            pre_desc = ""
            desc_after_span = ""

            # cap = "Район <span class='highlighted'>Гонконг</span>а Wan Chai, Гонконг, Hong Kong Island, САР Гонконг"
            while re.search(r"(?<='highlighted'>).+", cap_res):
                match = re.search(r"(?<='highlighted'>).+", cap_res)
                span_ind = match.group(0).index("</")
                help_txt = match.group(0)[:span_ind]
                pre_desc += help_txt
                cap_res = cap_res[match.span()[0]:]

            if re.search(r"(?<=span>).+", cap_res):
                desc_after_span = re.search(r"(?<=span>).+", cap_res).group(0).strip()

            description = f"{desc_before_span}{pre_desc}{desc_after_span}".strip()

            places.append(
                {
                    'dest_ID': j_data.get('destinationId'),
                    'name': j_data.get('name'),
                    'description': description
                }
            )

    return places
