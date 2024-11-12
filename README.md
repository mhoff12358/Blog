# My fork of SLIMEBLOGGER with my content in it

SLIMEBLOGGER made by slimelia (https://github.com/slimelia/slimeblogger)

## Build

cd build
python generatePages.py

## Markdown formatting

Web blog content is generated from Markdown blog post documents.
All blog posts must contain a header on the first line:

`@title Title Goes Here @date yyyy-mm-dd @perdayindex 4`

Posts are sorted by date, then by perdayindex (increasing)

Open the `build` directory in your terminal and run `pip install -r requirements.txt` to install requirements. Needs python >=3.11
