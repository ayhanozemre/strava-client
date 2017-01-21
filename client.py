import os
import logging
import requests

from settings import SECRET_KEY, API_ENDPOINT, DEFAULT_CITY_BOUNDS

logger = logging.getLogger(__name__)


def make_request(endpoint, method='get', data=None):
    headers = {'Authorization': 'Bearer %s' % SECRET_KEY}
    url = os.path.join(API_ENDPOINT, endpoint)
    return requests.request(method, url, data=data, headers=headers)


def prepare_request(*args, **kwargs):
    req = make_request(*args, **kwargs)
    if req.ok:
        return req.json()
    else:
        logger.warning('response is not json serializable')
    return {}


def make_segments_request(bounds=DEFAULT_CITY_BOUNDS):
    return prepare_request('segments/explore', data={'bounds': bounds})


def make_leaderboard_request(segment_id):
    uri = 'segments/{segment_id}/leaderboard'.format(segment_id=segment_id)
    return prepare_request(uri, data={'per_page': 50})


def get_segments():
    segments_response = make_segments_request()
    return segments_response.get('segments', [])


def get_leaderboard_entries(segment_id):
    leaderboard_response = make_leaderboard_request(segment_id)
    return leaderboard_response.get('entries', [])


def get_entrie_score(entrie):
    rank = entrie['rank']
    speed = entrie['distance'] / entrie['moving_time']
    average_watts = entrie['average_watts'] or 1
    average_hr = entrie['average_hr'] or 1
    avarage_hw = average_hr / average_watts
    return int(sum((speed, rank, avarage_hw)))


def leaderboard_data_handler():
    segments = get_segments()
    intersection_entries = {}
    for segment in segments:
        entries = get_leaderboard_entries(segment['id'])
        for entrie in entries:
            entrie['shots_count'] = 1
            athlete_id = entrie['athlete_id']
            intersection_entrie = intersection_entries.get(athlete_id)
            if intersection_entrie:
                entrie_ratio = get_entrie_score(entrie)
                intersection_entrie['entrie_ratios'].append(entrie_ratio)
                intersection_entrie['shots_count'] += 1
            else:
                entrie['entrie_ratios'] = [get_entrie_score(entrie)]
                intersection_entries[athlete_id] = entrie
    return intersection_entries.values()


def get_leaderboard_intersection():
    leaderboard_data = leaderboard_data_handler()
    entrie_list = []
    for entrie in leaderboard_data:
        if entrie['shots_count'] > 1:
            entrie_list.append(entrie)
    return entrie_list


def get_leaderboard_intersection_scores():
    intersection_list = get_leaderboard_intersection()
    entrie_list = []
    for entrie in intersection_list:
        entrie['score'] = sum(entrie['entrie_ratios'])
        entrie_list.append(entrie)
    return entrie_list
