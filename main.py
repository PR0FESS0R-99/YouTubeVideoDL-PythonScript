import yt_dlp

# Default download folder
DOWNLOAD_FOLDER = "downloads/"

def download_video(url):
    with yt_dlp.YoutubeDL() as ydl:
        try:
            # Extract video information
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get("formats", [])

            if not formats:
                print("No formats found.")
                return

            # Display all available formats
            print("Available formats:")
            for i, f in enumerate(formats):
                # Display video formats with their resolution and codec
                if "height" in f and f.get("vcodec") != "none":
                    print(
                        f"{i + 1}: Quality: {f.get('format_note')}, Resolution: {f.get('height')}p, Extension: {f.get('ext')}, Codec: {f.get('vcodec')}"
                    )

            # Ask user to select quality
            choice = int(input("Select quality by number: ")) - 1
            if 0 <= choice < len(formats):
                selected_format = formats[choice]
                format_id = selected_format.get("format_id", "bestvideo")

                ydl_opts = {
                    "format": format_id,
                    "outtmpl": DOWNLOAD_FOLDER
                    + "%(title)s.%(ext)s",  # Save file in default folder
                    "merge_output_format": "mkv",  # Ensure output is in mkv format
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            else:
                print("Invalid choice!")

        except yt_dlp.utils.ExtractorError as e:
            print(f"ExtractorError: {e}")
        except yt_dlp.utils.DownloadError as e:
            print(f"DownloadError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    download_video(video_url)
