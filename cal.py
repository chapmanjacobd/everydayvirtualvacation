from ics import Calendar, Event
from datetime import date, timedelta

from db import fetchall_dict
from rich import print
from flag import flag

c = Calendar()


def add_allday_event(c, event_start, event_name, event_description):
    e = Event()
    e.name = event_name
    e.description = event_description
    e.begin = event_start.isoformat()
    e.end = (event_start + timedelta(days=1)).isoformat()
    e.make_all_day()
    c.events.add(e)


cities = fetchall_dict(
    """
select
    u
    , c.n
    , concat_ws(', ', c.s,c.c) s
    , v.video
from cities c
JOIN videos v ON v.id = c.id
order by (rank < 3500 and c.id < 3500) DESC
    , ROW_NUMBER() OVER ( PARTITION BY u ) -- prefer to show many countries
    , random()
--limit 2
"""
)

START_DATE = date.today()
for city in cities:
    print(city)

    add_allday_event(
        c,
        event_start=START_DATE,
        event_name=flag(city["u"]) + " " + city["n"],
        event_description=f"""{city["n"]} welcomes you !

{city["video"]}

{city["s"]}
    """,
    )

    START_DATE += timedelta(2)

c.events
with open("my.ics", "w") as my_file:
    my_file.writelines(c)
