# This tag should match the release tag in Github
TAG = "Topic_Venue_month_day_year"

all: render-talk push-talk render-site push-site

render-talk:
	-git rm -rf docs/*
	cd talk && quarto render talk.qmd
	python setup_redirect.py
	git add docs/talk/index.html
	-git add talk/talk.qmd

push-talk:
	-git add docs/talk/*
	-git add docs/talk/images/*
	-git add talk/images/*
	git commit -a -m"updating changed files"
	git push origin main

render-site:
	-rm docs/index.html
	-git commit -a -m"updating site files"
	cd site && quarto render index.qmd

push-site:
	git add docs/*
	git add -u
	git commit -m"updating changed files"
	git push origin main

# NOTE: pdf rendering doesn't work well using decktape
# a better solution is to print from chrome
# but the PDFs are often too large for github anyway

render-pdf:
	-mkdir docs/pdfs
	decktape reveal -s 1920x1080 docs/talk/talk.html docs/pdfs/$(TAG).pdf

push-pdf:
	git add docs/pdfs/$(TAG).pdf
	git commit -m"adding pdf [skip ci]"
	git push origin main

