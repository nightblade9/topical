# Tropical

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

# Designing a Theme

TBD. For now, inspect the existing ones and code and reverse-engineer how they work. Quick reference below.

Note that all CSS and images must be embedded within `layout.html` itself, because we can't guarantee/support path rewriting or using absolute directories (makes previewing your changes a pain otherwise).

## layout.html

- `content`: actual content (e.g. list of snippets)
- `siteName`: site name (from config)
- `pageTitle`: specific page title (e.g. "JRPG tag")

# snippet.html

- `title`: Page title. Gets converted into a link to the URL.
- `url`: Page URL. Converted to a link.
- `tags`: each is individually wrapped in `span class="tag"`
- `blurb`: blurb (if specified)