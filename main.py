import asyncio
import json
import os
from datetime import datetime
from json import JSONDecodeError
from aiohttp import ClientSession
from lxml import html
import asyncpg

from constants import headers, XPATH
from settings import CONFIG_FILE, DATETIME_FORMAT, db_credentials


async def insert_record(record):
    conn = await asyncpg.connect(**db_credentials)

    sql = '''INSERT INTO articles(url,title,body) VALUES ($1, $2, $3)'''
    await conn.execute(sql, *record)

async def parse_content(content):
    document = html.fromstring(content)
    title = ''.join(document.xpath(XPATH['title'])).strip()
    body = ''.join(document.xpath(XPATH['body'])).strip()
    return [title, body]

async def fetch_url(url):
    print('process', url)
    record = [url]

    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            page_content = await response.read()

    parse_data = await parse_content(page_content)
    record.extend(parse_data)

    try:
        await insert_record(record)
    except asyncpg.InvalidPasswordError:
        print('invalid credentials')

    print(f'{url} - done')

async def track_schedule(loop):
    config_data, parsed, change_time = {}, {}, None

    while True:
        try:
            new_time = os.stat(CONFIG_FILE).st_mtime
        except FileNotFoundError as e:
            print(e)
            continue

        if change_time != new_time:
            change_time = new_time
            parsed = {}
            try:
                with open(CONFIG_FILE) as config_file:
                    config_data = json.load(config_file)
            except JSONDecodeError as e:
                print(e)
                continue

        for task_name, task in config_data.items():
            export_time = datetime.strptime(task['date'], DATETIME_FORMAT)
            if export_time > datetime.now() or task_name in parsed:
                continue

            parsed[task_name] = task['date']
            [asyncio.ensure_future(fetch_url(url)) for url in task['urls']]

        await asyncio.sleep(60)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(track_schedule(loop))
    loop.close()

if __name__ == '__main__':
    main()