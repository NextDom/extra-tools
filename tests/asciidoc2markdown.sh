#!/bin/bash

# Adapted from https://tinyapps.org/blog/nix/201701240700_convert_asciidoc_to_markdown.html
# Using asciidoctor 1.5.6.1 and pandoc 2.0.0.1
# Install pandoc and asciidoctor

if [ -f /etc/redhat-release ]; then
	su - c "dnf install asciidoctor pandoc"
fi

if [ -f /etc/lsb-release ]; then
	sudo apt install asciidoctor
	wget https://github.com/jgm/pandoc/releases/download/2.0.0.1/pandoc-2.0.0.1-1-amd64.deb
	sudo dpkg -i pandoc-2.0.0.1-1-amd64.deb
fi


# Convert asciidoc to docbook using asciidoctor

asciidoctor -b docbook index.asciidoc

# foo.xml will be output into the same directory as foo.adoc

# Convert docbook to markdown

pandoc -f docbook -t gfm index.xml -o index.md

# Unicode symbols were mangled in foo.md. Quick workaround:

iconv -t utf-8 index.xml | pandoc -f docbook -t gfm | iconv -f utf-8 > index.md

# Pandoc inserted hard line breaks at 72 characters. Removed like so:

pandoc -f docbook -t gfm --wrap=none # don't wrap lines at all

pandoc -f docbook -t gfm --columns=120 # extend line breaks to 120

