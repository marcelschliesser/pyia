import os
import json
import shutil
import tempfile
import argparse
import itertools
import urllib.parse
import urllib.request
import concurrent.futures


base = 'https://web.archive.org'


def archive_urls(domain, start, end):
    """
    Return a list of archive urls for a given domain.
    """

    params = {
        'url': domain,
        'matchType': 'domain',
        'filter': 'statuscode:200',
        'from': start,
        'to': end,
        'output': 'json'
    }
    url = base + '/cdx/search/cdx?' + urllib.parse.urlencode(params)
    req = urllib.request.urlopen(url)
    res = req.read()
    return json.loads(res.decode("utf-8"))[1:]


def group_archive_urls(urls):
    """
    Group urls by the url key and keep latest entry.
    """

    sorted(urls, key=lambda x: x[0])
    urls = [
        list(group) for _, group in itertools.groupby(urls, lambda x: x[0])
        ]
    return [max(i, key=lambda x:int(x[1])) for i in urls]


def download_ressource(url):
    """
    Download resource from wayback machine server.
    """

    f = open(os.path.join(os.getcwd(), "data", "metadata.csv"), "a")
    with urllib.request.urlopen(url) as response:
        content_type = response.info().get_content_subtype()
        final_dir = os.path.join(os.getcwd(), 'data', content_type)
        os.makedirs(final_dir, exist_ok=True)
        with tempfile.NamedTemporaryFile(
                suffix=f'.{content_type}',
                delete=False,
                dir=final_dir) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
            f.write(f"'{tmp_file.name}','{url}'\n")
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', required=True)
    parser.add_argument('--start', required=True)
    parser.add_argument('--end', required=True)
    args = parser.parse_args()

    urls = archive_urls(args.domain, args.start, args.end)
    grouped_urls = group_archive_urls(urls)
    uris = map(lambda x: base + f'/web/{x[1]}if_/{x[2]}', grouped_urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_ressource, uris)


if __name__ == "__main__":
    main()
