# Configuration file for the Sphinx documentation builder.

from pathlib import Path

DIR = Path(__file__).parent.resolve()

# -- Project information

project = 'XSMP Modeler'
copyright = '2023, Thales Alenia Space'
author = 'Thales Alenia Space'

# -- General configuration

extensions = [
    "breathe",
    "sphinx_copybutton",
    "sphinxcontrib.rsvgconverter",
    "sphinxcontrib.moderncmakedomain",
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = "furo"

# -- Options for EPUB output
epub_show_urls = 'footnote'

def prepare(app):
    with open(DIR.parent.parent / "README.rst") as f:
        contents = f.read()

    if app.builder.name == "latex":
        # Remove badges and stuff from start
        contents = contents[contents.find(r".. start") :]

        # Filter out section titles for index.rst for LaTeX
        contents = re.sub(r"^(.*)\n[-~]{3,}$", r"**\1**", contents, flags=re.MULTILINE)

    with open(DIR / "readme.rst", "w") as f:
        f.write(contents)


def clean_up(app, exception):  # noqa: ARG001
    (DIR / "readme.rst").unlink()

def setup(app):
    # Copy the readme in
    app.connect("builder-inited", prepare)

    # Clean up the generated readme
    app.connect("build-finished", clean_up)
