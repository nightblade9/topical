# Tropical

[![Build Status](https://travis-ci.com/nightblade9/tropical.svg?branch=main)](https://travis-ci.com/nightblade9/tropical)

Static website generator for link collections with metadata. Features:

- Quickly generates a static site with metadata (tags, blurb, etc.) for creating topical sites on a topic
- Can be hosted for free on GitHub via GitHub Pages
- Includes client-side search

# Sites Built with Tropical

Open an issue/PR to get your Tropical-based site listed here.
 
- [Game Design Library](https://nightblade9.github.io/game-design-library)

# Usage

Create a new directory for your tropical project. (Bonus points if you version-control it.) Within that directory, create a file called `data.json`. Each entry needs:

- a `title`
- a `url`
- One or more `tags`

Optionally, you can include:
- a `blurb` describing the link
- an `type` - if specified, Tropical will add `/images/<type>.png` after the item title 

```json
[
    {
        "title": "Steambirds: Survival Mobile",
        "url": "https://lostgarden.home.blog/2011/10/13/steambirds-survival-mobile/",
        "tags": ["arrow of play", "game analysis", "choice", "pacing", "goals"],
        "blurb": "An introduction to the concept of arrow of play, the property of systems that always move the player forward (such as hunger in roguelikes)."
    },
    {
        "title": "How to Keep Players Engaged (Without Being Evil)",
        "url": "https://www.youtube.com/watch?v=hbzGO_Qonu0",
        "tags": ["engagement", "pacing", "intensity", "difficulty", "core loop", "goals"],
        "blurb": "How to keep players engaged, without addictive evil design?",
        "type": "video"
    }
]
```

Next, copy the `default-theme` directory from `tropical` to your project root and rename it to `theme`.

Finally, run `tropical` to generate the output.  I haven't bundled this as a `pip` module yet, so for now, you need to run it by hand.

- `git clone https://github.com/nightblade/tropical`
- `cd tropical`
- `python main.py /path/to/project/folder`

You can customize the theme by hand as you wish, or replace it outright.

# Additional Configuration

## config.json

You can include a `config.json` file in your project directory with the following fields:

- `siteRootUrl`: the root URL of your site. All links point to this. For debugging locally, set this to empty string. If the config file is missing or the value is empty, links assume the root directory, e.g. the tags page links `/tags/index.html`.

If you would like to add OpenGraph tags to each of your pages automatically, please add an `openGraph` property with the following values:

- `title`: The title of the website (used in `<og:title>` tag)
- `image`: The URL to the image used in the OpenGraph thumbnails, relative to `siteRootUrl`
- `description`: The site description (used in `<og:description>` tag)

Note that the title and description will be prefixed with page-specific values, such as `Items tagged with JRPG - {description}`.

Sample:

```json
    "siteRootUrl": "https://nightblade9.github.io/game-design-library",
    "openGraph": {
        "title": "Game Design Library",
        "image": "images/openGraph.png",
        "description": "A library of game-design articles that deal with topics like lives, balancing difficulty, perfecting your core loop, loot-boxes, and player experience"
    }
}
```

You can also overwrite the `siteRootUrl` value from the command-line by specifying `--localhost` as an argument to `tropical`; this will ignore the value in `config.json` and instead specify `localhost:8000`.

## tags.json

You can include a `tags.json` file with a description of each tag. It will appear on the tag's page, under the title (e.g. "8 items tagged with JRPG").

Sample:

```json
{
    "JRPG": "Junior rocket-powered gorrila",
    "idle": "What it's called when you do nothing"
}
```

To see which tags don't have a corresponding entry in `tags.json`, run `tropical` with the command-line argument `--report-missing-tag-descriptions`

# How Search Works

Since Tropical generates static sites, we can't track which links are more or less popular, or scan an article's contents for relevancy. Instead, we look at the title, tags, and blurb. 

For every word the user searches for, if that word appears in any of the fields specified above, that increases the rank of that article for that search.

Tropical uses a weighted average:
- title matches are worth 2 points per search word
- tag matches are worth 1 point per search word
- blurb matches are worth 4 points per search word

While blurbs are optional, if search is important to your site, we highly recommend writing terse, keyword-packed blurbs; it will dramatically improve the quality of search results.

# Additional Pages

You can add additional static HTML pages to your project; simply create a `pages` directory and add any `.html` files. Like other files, they will be combined with the theme and copied to the output directory.

# Local Development

You need Python 3.5+ and a modern browser (i.e. not IE6-8). To run locally, just run `python main.py <path to project repo>`, then from the `output` directory, run `python -m http.server` and hit up `localhost:8000`.

# Designing a Theme

TBD. For now, inspect the existing ones and code and reverse-engineer how they work. Quick reference below.

Note that any external directories (images, CSS, JS, etc.) - but not files - will be copied from the theme directory to the output directory when you build the website. We highly recommend organizing all assets into directories within your theme.

Also note that any HTML files in your project directory get copied over as-is, albeit with substitutions for tokens below (specifically, `siteRootUrl` gets substituted in if you specified it in `config.json`)

## Pages

### layout.html

- `{content}`: actual content (e.g. list of snippets)
- `{pageTitle}`: specific page title (e.g. "JRPG tag")
- `{search}`: the search form
- `{siteRootUrl}`: the root URL of the site, from the config file (`config.json`)

### snippet.html

- `{title}`: Page title. Gets converted into a link to the URL.
- `{url}`: Page URL. Converted to a link.
- `{tags}`: each is individually wrapped in `span class="tag"`
- `{blurb}`: blurb (if specified)

### intro.html (optional)

If present, a small intro blurb will be shown on the home page, using the contents of this file. 

- `{stats}`: Site stats (number of items catalogued and number of tags).
- `{tags:n}`: Shows the most popular `n` tags, descending (most-popular first).
- `{lastUpdated}`: Shows the date Tropical generated the site.
- `{itemsOnHomePage}`: Specifies how many items to show on the home page. Also causes `all.html` to generate with a list of all items.

## CSS

Tropical emits a number of CSS classes to allow you to style things how you like. Check the sample theme for examples.