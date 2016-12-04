import argparse
import os
import requests
from git import Repo


def main():
    parser = argparse.ArgumentParser(description="A tool to clone github only repositories of user or group")
    parser.add_argument("--u", help="target of massive download",
                        dest='target', required=True)
    parser.add_argument("--o", help="Directory to save repos at",
                        dest='out', required=False)
    args = parser.parse_args()
    target = args.target
    if not target:
        print("ERROR: You need to specify target, ex: gitdown -u dex73r")
        return 1
    output = args.out
    if not output:
        output = target
    pageNumber = 1
    while (pageNumber > 0):
        url = ("https://api.github.com/users/%s/repos?page=%i&per_page=100" % (target, pageNumber))
        j = requests.get(url).json()
        pageCount = len(j)
        if (pageCount < 1):
            pageNumber = -1
        for el in j:
            print(el["git_url"])
            gitlink = el["git_url"]
            out_name = os.path.join(output, el["name"])
            if os.path.isdir(out_name):
                repo = Repo(out_name)
                repo.remotes.origin.pull()
            else:
                Repo.clone_from(gitlink, out_name)

        pageNumber = pageNumber + 1
    return 1337


if __name__ == "__main__":
    main()
