import yt_dlp
import os

video_links = [
    "https://video.squarespace-cdn.com/content/v1/65568ba172adb3569940fea7/ca178815-ee55-4004-bb7c-fa2e3f325fe6/playlist.m3u8",
    "https://video.squarespace-cdn.com/content/v1/65568ba172adb3569940fea7/e06c714a-1b1e-4ff3-ac39-f3c25d953078/playlist.m3u8",
]

video_names = [
    "bhutan_traffic",
    "bhutan_archery",
]

for i, video_url in enumerate(video_links):
    # Get the corresponding name from the video_names list
    base_name = video_names[i]

    # Clean the name to be safe for filenames (remove/replace invalid characters)
    # This is a basic cleaning; you might need more robust handling for complex names
    safe_base_name = "".join(
        c for c in base_name if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    safe_base_name = safe_base_name.replace(
        " ", "_"
    )  # Replace spaces with underscores for cleaner filenames

    # Construct the full output path and filename
    # We'll stick to .mp4 as the merge_output_format is mp4
    output_filename = os.path.join("downloads", f"{safe_base_name}.mp4")

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
        "verbose": True,  # Set to False to suppress detailed output, True for debugging
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n--- Attempting to download: '{base_name}' from {video_url} ---")
            ydl.download([video_url])
        print(f"--- Successfully processed: '{output_filename}' ---")
    except Exception as e:
        print(
            f"--- An error occurred downloading '{video_url}' as '{base_name}': {e} ---"
        )
