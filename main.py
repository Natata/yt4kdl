import yt_dlp
import argparse
import os

class YouTubeDownloader:
    def __init__(self, output_path="downloads"):
        """Initialize the downloader with an output path."""
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def download_video(self, url, quality="2160"):
        """
        Download a YouTube video in specified quality.
        
        Args:
            url (str): YouTube video URL
            quality (str): Preferred video quality (2160 for 4K, 1080 for Full HD, etc.)
        """
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\nFetching video information...")
                info = ydl.extract_info(url, download=False)
                print(f"\nTitle: {info['title']}")
                print(f"Duration: {info['duration']} seconds")
                print(f"\nStarting download...")
                ydl.download([url])
                print("\nDownload completed successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def progress_hook(self, d):
        """Display download progress."""
        if d['status'] == 'downloading':
            percentage = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\rDownloading... {percentage} at {speed}", end='')
        elif d['status'] == 'finished':
            print("\nDownload finished. Now post-processing...")

def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos in high quality.')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--output', '-o', default='downloads',
                       help='Output directory for downloaded videos')
    parser.add_argument('--quality', '-q', default='2160',
                       help='Preferred video quality (2160 for 4K, 1080 for Full HD, etc.)')
    
    args = parser.parse_args()
    
    downloader = YouTubeDownloader(args.output)
    downloader.download_video(args.url, args.quality)

if __name__ == "__main__":
    main()
