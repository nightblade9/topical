from tropical.constants import STATIC_CONTENT_DIRECTORY, OPEN_GRAPH_TEMPLATE_FILE

class OpenGraphGenerator:
    def __init__(self, config):
        if "siteRootUrl" in config and "openGraph" in config:
            self._config = config

            self._can_generate = True
            with open("{}/{}".format(STATIC_CONTENT_DIRECTORY, OPEN_GRAPH_TEMPLATE_FILE)) as file_handle:
                self._open_graph_template = file_handle.read()
    
    def add_meta_tags(self, html, title_prefix):
        meta_tags = self._generate_meta_tags(title_prefix)
        return html.replace("</head>", "{}{}".format(meta_tags, "</head>"))

    def _generate_meta_tags(self, title_prefix):
        # Don't have siteRootUrl and OpenGraph in config.json? Can't do nothin'
        if not self._can_generate:
            return ""
        
        open_graph_config = self._config["openGraph"]

        title = open_graph_config["title"]
        if title_prefix != "":
            title = "{} - {}".format(title_prefix, title)

        meta_tags = self._open_graph_template \
            .replace("{title}", title) \
            .replace("{siteRootUrl}", self._config["siteRootUrl"]) \
            .replace("{imageUrl}", open_graph_config["image"]) \
            .replace("{description}", open_graph_config["description"])

        return meta_tags