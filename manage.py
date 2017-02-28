from flask import Flask, jsonify, url_for
from client import (get_leaderboard_intersection_scores,
                    get_leaderboard_intersection)

app = Flask(__name__)

EXCLUDE_ENDPOINTS = ['static']


@app.route("/")
def home():
    url_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint in EXCLUDE_ENDPOINTS:
            continue
        uri = url_for(rule.endpoint)
        label = uri.replace('-', ' ')
        label = label.title()
        href = '<a href="{uri}">{label}</a>'.format(uri=uri, label=label)
        url_list.append(href)
    response = '<br>'.join(url_list)
    return response


@app.route("/leaderboard-intersection")
def leaderboard_intersection_view():
    data = get_leaderboard_intersection()
    return jsonify(data)


@app.route("/leaderboard-intersection-scores")
def leaderboard_intersection_score_view():
    data = get_leaderboard_intersection_scores()
    return jsonify(data)


if __name__ == "__main__":
    app.run()
