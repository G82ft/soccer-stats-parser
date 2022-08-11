import json
import re
from typing import Generator

import requests
from bs4 import BeautifulSoup

URL: str = 'https://nb-bet.com'
HEADERS: dict = {
    "Accept": '*/*',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}
SESSION = requests.session()


def get_leagues() -> Generator[tuple[str, str], None, None]:
    url: str = 'https://app.nb-bet.com/v1/page-soccer-leagues/{}/0/true/120/0/true/1/false'
    page: int = 1
    leagues: list[dict, ...] = [{}, ]
    while leagues:
        r = SESSION.get(url.format(page))

        if not r.ok:
            yield r.status_code
            break

        leagues = r.json()["data"]["leagues"]

        for L in leagues:
            yield L["1"], L["2"][13:]  # Slicing out '/Tournaments/'

        page += 1


def get_teams(link: str) -> Generator[tuple[str, str], None, None]:
    r = SESSION.get(f"{URL}/Tournaments/{link}", headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_="table-summary")

    if table is None:
        return

    for tr in table('tr', class_=re.compile("tournaments-stats-cells")):
        team_cell = tr.find('a')
        yield team_cell.text, team_cell["href"][7:]  # Slicing out '/Teams/'


def get_rows(league_id: int, team: tuple[str, str], amount: int, current_season: bool, at_home: bool) -> int | tuple:
    url = ("https://app.nb-bet.com/v1/page-soccer-team/"
           f"{team[1]}/{amount}/{league_id}/"
           f"{json.dumps(current_season)}/true/{json.dumps(at_home)}/{json.dumps(not at_home)}/false")

    r = SESSION.get(url, headers=HEADERS)

    if not r.ok:
        return team[0], None

    match_team_info = r.json()["data"]["team"]["12"][0][0]

    if not match_team_info:
        return team[0], None

    if "20" not in match_team_info:
        return team[0], None

    amount = match_team_info["1"]
    av_shot_on_goal = match_team_info["20"]
    av_goal = match_team_info["8"]
    av_missed_shot_on_goal = match_team_info["21"]
    av_missed_goal = match_team_info["9"]

    return team[0], amount, av_shot_on_goal, av_goal, av_missed_shot_on_goal, av_missed_goal


def dump_to_table() -> Generator[int, None, None]:
    pass


def main() -> None:
    pass


main()

for i in get_leagues():
    for j in get_teams(i[1]):
        get_rows(i[1].split('-')[0], j, 10, True, True)
