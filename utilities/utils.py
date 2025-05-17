import html2text


def clean_markdown(html: str) -> str:
    if not html:
        return ""

    h = html2text.HTML2Text()
    h.body_width = 0  # Prevent line wrapping
    h.ignore_links = False  # Keep links
    h.inline_links = True  # Use inline links (more compact)

    # Options to remove unnecessary content
    h.ignore_images = True
    h.ignore_emphasis = True
    h.ignore_tables = True
    h.single_line_break = True
    h.unicode_snob = False
    h.wrap_links = False
    h.mark_code = False
    h.pad_tables = False
    h.escape_snob = False
    h.skip_internal_links = True
    h.ignore_anchors = True

    markdown = h.handle(html)
    return markdown.strip()


# def compare_date(start_date: str, end_date: str, article_date: str):
#     if (article_date) and parse(article_date) and (end_date):
#             if (parse(item.date) >= parse(oldest_date)) and (
#                 parse(item.date) <= parse(earliest_date)
#             ):
#
