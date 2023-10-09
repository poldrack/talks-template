# configure scripts for the talk

import os
import sys
import git
import toml

def load_toml(tomlfile="config.toml"):
    try:
        import toml
    except ImportError:
        print("Please install toml package")
        sys.exit(1)

    try:
        with open(tomlfile) as f:
            config = toml.load(f)
    except FileNotFoundError:
        print(f"Please create {tomlfile}")
        sys.exit(1)

    return config

def get_current_repo_remote():
    repo = git.Repo(search_parent_directories=True)
    if len(repo.remotes) == 0:
        raise Exception("No remote repository found.")

    remote = repo.remotes[0]

    urls = list(remote.urls)

    if len(urls) == 0:
        raise Exception("No remote branch found.")

    return(urls[0])


def get_talk_url(config):
    url_split = config['remote'].split("/")
    talk_url = f"{config['base_url']}/{url_split[1].split('.')[0]}/talk/talk.html"
    return(talk_url)


def get_repo_url(config):
    url_split = config['remote'].split("/")
    repo_url = f"{config['base_url']}/{url_split[1].split('.')[0]}"
    return(repo_url)


class ConfigurationError(Exception):
    "Raised when user has not configured the config.toml file yet."
    pass


def fix_makefile(config):
    with open("Makefile", "r") as f:
        makefile = f.read()

    replace_tag = "Topic_Venue_month_day_year"
    if replace_tag == config['tag']:
        raise ConfigurationError("Please configure config.toml file before running this script.")

    if replace_tag not in makefile and config['tag'] in makefile:
        print("Tag is already set in Makefile")
        return
    print(f"Replacing {replace_tag} with {config['tag']} in Makefile")
    makefile = makefile.replace(replace_tag, config['tag'])
    with open("Makefile", "w") as f:
        f.write(makefile)


def fix_readme(config):

    readme = f"""# {config['title']}

This talk repository is based on the [talk template](https://github.com/poldrack/talks-template).  

The latest version of the talk is available at {config['talk_url']}

    """

    with open("README.md", "w") as f:
        f.write(readme)


def fix_site(config, backup=True):
    with open("site/index.qmd", "r") as f:
        index = f.read()
    index = index.replace(
        "Talks about the template project", 
        f"Talks about {config['title']}")
    
    if backup:
        os.rename("site/index.qmd", "site/index.qmd.bak")

    with open("site/index.qmd", "w") as f:
        f.write(index)
    
    with open('site/_quarto.yml', 'r') as f:
        quarto = f.read()
    
    quarto = quarto.replace(
        "Template talk", 
        config['title'])
    quarto = quarto.replace(
        "https://github.com/poldrack/talks-template",
        config['repo_url'])

    with open("site/_quarto.yml", "w") as f:
        f.write(quarto)

def fix_talk(config, backup=True):
    with open("talk/talk.qmd", "r") as f:
        talk = f.read()
    talk = talk.replace(
        "Talk template", 
        config['title'])
    talk = talk.replace(
        "https://poldrack.github.io/talks-template/",
        config['repo_url'])

    if backup:
        os.rename("talk/talk.qmd", "talk/talk.qmd.bak")

    with open("talk/talk.qmd", "w") as f:
        f.write(talk)

def write_config(config, backup=True):
    if backup:
        os.rename("config.toml", "config.toml.bak")
    with open("config.toml", "w") as f:
        f.write(toml.dumps(config))


if __name__ == "__main__":
    config = load_toml()
    config['remote'] = get_current_repo_remote()
    config['talk_url'] = get_talk_url(config)
    config['repo_url'] = get_repo_url(config)

    print(config)

    fix_makefile(config)
    fix_readme(config)
    fix_site(config)
    fix_talk(config)


    write_config(config)
