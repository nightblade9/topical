# Tropical

[![Build Status](https://travis-ci.com/nightblade9/tropical.svg?branch=main)](https://travis-ci.com/nightblade9/tropical)

Static website generator for link collections with metadata. Features:

- Quickly generates a static site with metadata (tags, blurb, etc.) for creating topical sites on a topic
- Can be hosted for free on GitHub via GitHub Pages
- Includes client-side search

# Usage

Create a new directory for your tropical project. (Bonus points if you version-control it.) Within that directory, create a file called `data.json`. Each entry needs a `title`, `url`, and `tags`; `blurb` is optional. Example:

```json
[
    {
        "title": "Pelican",
        "url": "https://docs.getpelican.com/en/latest/",
        "tags": [ "static-site-generator", "python" ],
        "blurb": "Static site generator that supports Markdown."
    },
    {
        "title": "Wordpress",
        "url": "https://wordpress.org",
        "tags": [ "cms", "php", "mysql" ]
    }
]
```

Next, copy the `default-theme` directory from `tropical` to your project root and rename it to `theme`.

Finally, run `tropical` to generte the output.  I haven't bundled this as a `pip` module yet, so for now, you need to run it by hand.

- `git clone https://github.com/nightblade/tropical`
- `cd tropical`
- `python main.py /path/to/project/folder`

You can customize the theme by hand as you wish, or replace it outright.

# Additional Configuration

You can include a `config.json` file in your project directory with the following fields:

- `siteRootUrl`: the root URL of your site. All links point to this. For debugging locally, set this to empty string. If the config file is missing or the value is empty, links assume the root directory, e.g. the tags page links `/tags/index.html`.

# Additional Pages

You can add additional static HTML pages to your project; simply create a `pages` directory and add any `.html` files. Like other files, they will be combined with the theme and copied to the output directory.

# Local Development

You need Python 3.5+ and a modern browser (i.e. not IE6-8). To run locally, just run `python main.py <path to project repo>`, then from the `output` directory, run `python -m http.server` and hit up `localhost:8000`.

# Designing a Theme

TBD. For now, inspect the existing ones and code and reverse-engineer how they work. Quick reference below.

Note that any external directories (images, CSS, JS, etc.) - but not files - will be copied from the theme directory to the output directory when you build the website. We highly recommend organizing all assets into directories within your theme.

## layout.html

- `{content}`: actual content (e.g. list of snippets)
- `{siteName}`: site name (from config)
- `{pageTitle}`: specific page title (e.g. "JRPG tag")
- `{search}`: the search form

# snippet.html

- `{title}`: Page title. Gets converted into a link to the URL.
- `{url}`: Page URL. Converted to a link.
- `{tags}`: each is individually wrapped in `span class="tag"`
- `{blurb}`: blurb (if specified)

## intro.html (optional)

If present, a small intro blurb will be shown on the home page, using the contents of this file. 

- `{stats}`: Site stats (number of items catalogued and number of tags).