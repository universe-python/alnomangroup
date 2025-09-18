from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(value):
    parsed_url = urlparse(value)
    if "youtu.be" in parsed_url.netloc:  # Shortened YouTube URL
        video_id = parsed_url.path[1:]  # Extract the path after '/'
    elif "youtube.com" in parsed_url.netloc and "/watch" in parsed_url.path:  # Full YouTube URL
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
    elif "youtube.com" in parsed_url.netloc:  # Extract Embed URL
        video_id = parsed_url.path[7:]
    else:
        return value  # Return as-is if not a valid YouTube link

    # Construct the embed URL
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return value  # Return as-is if no video ID found


