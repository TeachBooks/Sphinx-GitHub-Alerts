import re

from sphinx.util import logging
from sphinx.errors import ConfigError

logger = logging.getLogger(__name__)

RECOGNISED_TYPES = {
    'note': 'note',
    'tip': 'tip',
    'important': 'important',
    'warning': 'warning',
    'caution': 'caution',
}

def validate_sphinx_github_alerts_config(app, config):
    """Validate sphinx_github_alerts__config."""
    redirects = getattr(config, 'sphinx_github_alerts_redirects', {})
    # convert all keys and values to lowercase
    redirects = {k.lower(): v.lower() for k, v in redirects.items()}
    app.config.sphinx_github_alerts_redirects = redirects
    if not isinstance(redirects, dict):
        raise ConfigError("sphinx_github_alerts_redirects must be a dict.")
    invalid = set(redirects.keys()) - set(RECOGNISED_TYPES.keys())
    if invalid:
        raise ConfigError(f"sphinx_github_alerts_redirects has invalid keys: {sorted(invalid)}. "
                          f"Allowed keys: {sorted(RECOGNISED_TYPES.keys())}")
    # validate leading spaces
    leading_spaces = getattr(config, 'sphinx_github_alerts_leading_spaces', None)
    if not isinstance(leading_spaces, int) or leading_spaces < 1:
        raise ConfigError("sphinx_github_alerts_leading_spaces must be an integer >= 1.")
    # validate backquotes
    backquotes = getattr(config, 'sphinx_github_alerts_backquotes', None)
    if not isinstance(backquotes, int) or backquotes < 3:
        raise ConfigError("sphinx_github_alerts_backquotes must be an integer >= 3.")

def convert_github_alerts(app, docname, source):
    source_file = app.env.doc2path(docname)
    if not(source_file.endswith('.md') or source_file.endswith('.ipynb') or source_file.endswith('.rst')):
        logger.warning(f"Unrecognised source file type for '{source_file}', skipping...",location=docname)
        pass
    """Replace GitHub alerts with Sphinx admonitions."""

    # Find any block starting with '> [!type] and replace it
    # with the appropriate admonition syntax for Sphinx.'
    # type can only be one of 'note', 'tip', 'important', 'warning', 'caution', etc.
    # Capitalization does not matter.

    # Find each block within the source
    content = source[0]
    # store old content for comparison
    old_content = content
    
    # Pattern to find consecutive lines starting with '>'
    if source_file.endswith('.ipynb'):
        pattern = r'^(?:\s*\">.*\n?)+' # Matches one or more consecutive lines starting with '>', allowing leading spaces
        type_pattern = r'\s*\">\s*\[!(\w+)\]' # Pattern to extract type from first line, allowing leading spaces
        strip_pattern = r'^\s*\">\s?' # Pattern to strip leading '> ' from each line
        new_pattern = r'"'
        arrows_pattern = r'^\s*\"(?:>\s*)+'
    else: # meaning .md or *.rst
        pattern = r'^(?:>.*\n?)+' # Matches one or more consecutive lines starting with '>'
        type_pattern = r'>\s*\[!(\w+)\]' # Pattern to extract type from first line
        strip_pattern = r'^>\s?' # Pattern to strip leading '> ' from each line
        new_pattern = r''
        arrows_pattern = r'^(?:>\s*)+'
    
    # Find all matches
    matches = re.finditer(pattern, content, re.MULTILINE)
    new_blocks = []

    EXTENDED_TYPES = RECOGNISED_TYPES.copy() | app.env.config.sphinx_github_alerts_redirects
    quotes = '`'*(app.env.config.sphinx_github_alerts_backquotes)

    for i,match in enumerate(matches):
        block = match.group(0)
        # Process each block here
        first_line = block.splitlines()[0]
        # extract type from first line and convert to lowercase
        type_match = re.search(type_pattern, first_line)
        if type_match: # do nothing if no type found
            type_match = type_match.group(1).lower()
            if type_match in EXTENDED_TYPES:
                # strip all > and leading spaces from each line in block
                # exclude first line
                stripped_block = '\n'.join([re.sub(strip_pattern, new_pattern, line) for line in block.splitlines()[1:]])
                # create replacement admonition block depending on original source type (.md, .ipynb or .rst)
                if source_file.endswith('.md'):
                    replacement = f"\n{quotes}{{{EXTENDED_TYPES[type_match]}}}\n{stripped_block}\n{quotes}\n"
                elif source_file.endswith('.ipynb'):
                    # make sure to add the necessary quotes and commas for ipynb format
                    if stripped_block[-1] == '"':
                        stripped_block = stripped_block[:-1] + '\\n",'
                        replacement = f"\n\"{quotes}{{{EXTENDED_TYPES[type_match]}}}\\n\",\n{stripped_block}\n\"{quotes}\\n\""
                    else:
                        replacement = f"\n\"{quotes}{{{EXTENDED_TYPES[type_match]}}}\\n\",\n{stripped_block}\n\"{quotes}\\n\",\n"
                elif source_file.endswith('.rst'):
                    replacement = f"\n.. {EXTENDED_TYPES[type_match]}:: \n\n"
                    # indent each line of stripped_block by set number of leading spaces
                    indent = " " * app.env.config.sphinx_github_alerts_leading_spaces
                    indented_block = '\n'.join([indent + line for line in stripped_block.splitlines()])
                    replacement += f"{indented_block}\n"
                # store the new block
                if replacement:
                    new_blocks.append(replacement)
                else:
                    new_blocks.append(block)
            else:
                # find the line number of the match in the content
                line_number = content[:match.start()].count('\n') + 1
                logger.warning(f"Unrecognised GitHub alert type '{type_match}', skipping...",location=(docname, line_number))
                new_blocks.append(block)
        else:
            new_blocks.append(block)
    
    # replace all blocks in content with new_blocks
    for match, new_block in zip(re.finditer(pattern, content, re.MULTILINE), new_blocks):
        content = content.replace(match.group(0), new_block)
    
    source[0] = content

    pass

def setup(app):

    app.add_config_value('sphinx_github_alerts_redirects', {}, 'html')
    app.add_config_value('sphinx_github_alerts_backquotes', 3, 'html')
    app.add_config_value('sphinx_github_alerts_leading_spaces', 3, 'html')
    app.connect('config-inited', validate_sphinx_github_alerts_config)
    app.connect('source-read', convert_github_alerts)
    
    return {
        "version": "builtin",
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }



