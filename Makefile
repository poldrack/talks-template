# This tag should match the release tag in Github
TAG = "Topic_Venue_Month_Day_Year"


all: render-talk render-pdf render-site

render-talk:
	-git rm -rf docs/talk/*
	cd talk && quarto render talk.qmd
	# fix quarto bug
	# need to use sed inline mode
	-git add docs/talk/*
	-git add docs/talk/images/*
	-git add talk/images/*
	# sed -i.bak 's-LICENSE-talk-' docs/talk/index.html
	git commit -a -m"updating changed files"
	git push origin main

render-site:
	-rm docs/index.html
	-git commit -a -m"updating site files"
	cd site && quarto render index.qmd
	git add docs/*
	git commit -m"updating changed files"
	git push origin main

render-pdf:
	-mkdir docs/pdfs
	decktape reveal docs/talk/talk.html docs/pdfs/$(TAG).pdf
	git add docs/pdfs/$(TAG).pdf
	git commit -m"adding pdf [skip ci]"
	git push origin main

