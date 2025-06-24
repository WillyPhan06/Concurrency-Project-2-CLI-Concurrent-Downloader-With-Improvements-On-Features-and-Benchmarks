import argparse
from downloader.threading_downloader import Threading_Downloader
from downloader.asyncio_downloader import Asyncio_Downloader
from downloader.multiprocessing_downloader import Multiprocessing_Downloader
from downloader.mix_downloader import Mix_Downloader
import sys

def main():
    parser = argparse.ArgumentParser(description="CLI Improved Concurrent Downloader")
    parser.add_argument("--method", choices=["asyncio", "multiprocessing", "threading","mix"], required=True, help="Choose a method to download urls")
    parser.add_argument("--url-file", required=True, help="Choose the correct url file to download urls inside it")
    parser.add_argument("--output-dir", required=True, help="Choose output directory to receive downloaded content from urls")
    args = parser.parse_args()

    try:
        with open(args.url_file, "r") as url_file:
            urls = [line.strip() for line in url_file if line.strip()]
    except Exception as e:
        print(f"❌ ERROR HAPPENED WHEN OPENING {args.url_file}: {e}")
        sys.exit(1)



    if args.method == "multiprocessing":
        downloader = Multiprocessing_Downloader(urls, args.output_dir)
    elif args.method == "asyncio":
        downloader = Asyncio_Downloader(urls, args.output_dir)
    elif args.method == "threading":
        downloader = Threading_Downloader(urls, args.output_dir)
    elif args.method == "mix":
        downloader = Mix_Downloader(urls, args.output_dir)
    else:
        print("❌ UNKNOWN METHOD TRY AGAIN")
        sys.exit(1)
    print(f"🚀 STARTING DOWNLOAD WITH {args.method.upper()} METHOD 🚀")
    downloader.download()

if __name__ == "__main__":
    main()
    
