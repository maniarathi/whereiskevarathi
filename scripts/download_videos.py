import yt_dlp
import os

import re

DOWNLOAD_DIRECTORY = "downloads"
ORIGINAL_CONTENT_DUMP = "original_squarespace_blogs.xml"


def extract_urls(text_dump):
    """
    Extracts URLs matching the pattern "https://video.squarespace-cdn.com/content/v1/65568ba172adb3569940fea7/{variable_string}/"
    from a given text dump.

    Args:
      text_dump: A string containing the text from which to extract URLs.

    Returns:
      A list of extracted URLs.
    """
    # The regex looks for:
    # - "https://" literal
    # - "video.squarespace-cdn.com/content/v1/" literal
    # - Then any characters (.*?) non-greedily up to the next slash
    # - "/" literal
    # - Then any characters ([^/]+) which are not a slash, one or more times, up to the end of the URL
    #   This ensures we capture the variable string after the last slash.
    pattern = r"https://video\.squarespace-cdn\.com/content/v1/65568ba172adb3569940fea7/[^/]+/"
    urls = re.findall(pattern, text_dump)
    print(f"Num URLs found: {len(urls)}")
    return set(urls)


def download_video(video_name, video_url):
    # Clean the name to be safe for filenames (remove/replace invalid characters)
    # This is a basic cleaning; you might need more robust handling for complex names
    safe_base_name = "".join(
        c for c in video_name if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    safe_base_name = safe_base_name.replace(
        " ", "_"
    )  # Replace spaces with underscores for cleaner filenames

    # Construct the full output path and filename
    # We'll stick to .mp4 as the merge_output_format is mp4
    output_filename = os.path.join(DOWNLOAD_DIRECTORY, f"{safe_base_name}.mp4")

    # Options for the download
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_filename,  # Manually specify the full output path and filename
        "merge_output_format": "mp4",  # Ensure the merged output is an MP4 file
        "postprocessors": [
            {
                "key": "FFmpegMetadata",  # Embeds metadata from the extracted info
                "add_chapters": False,
            }
        ],
        "retries": 5,  # Number of retries for failed downloads
        "fragment_retries": 5,  # Number of retries for fragmented downloads
        "concurrent_fragments": 5,  # Number of fragments to download concurrently
        "ignoreerrors": True,  # Continue even if an error occurs for one video
        "verbose": False,  # Set to False to suppress detailed output, True for debugging
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n--- Attempting to download: '{video_name}' from {video_url} ---")
            ydl.download([video_url])
        print(f"--- Successfully processed: '{output_filename}' ---")
    except Exception as e:
        print(
            f"--- An error occurred downloading '{video_url}' as '{video_name}': {e} ---"
        )


if __name__ == "__main__":
    f = open(ORIGINAL_CONTENT_DUMP)
    extracted_urls = extract_urls(f.read())
    f.close()

    for video_num, video_url in enumerate(extracted_urls):
        download_video(f"video_{video_num}", f"{video_url}playlist.m3u8")
        print(f"Downloaded video {video_num + 1} of {len(extracted_urls)}")
