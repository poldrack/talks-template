import git

repo = git.Repo('.')

if len(repo.remotes) == 0:
    raise Exception("No remote repository found.")

remote = repo.remotes[0]

urls = list(remote.urls)

if len(urls) == 0:
    raise Exception("No remote branch found.")

url = urls[0]
url_split = url.split("/")

talk_url = f"http://poldrack.github.io/{url_split[1].split('.')[0]}/talk/talk.html"

redirect = f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url='{talk_url}'" />
  </head>
  <body>
    <p>You will be redirected to the talk soon!</p>
  </body>
</html>
"""

with open("docs/talk/index.html", "w") as f:
    f.write(redirect)
