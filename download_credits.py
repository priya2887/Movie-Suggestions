import urllib.request
import os
import sys

urls = [
    "https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_credits.csv",
    "https://raw.githubusercontent.com/pxxthik/Movie-recommender-system/master/tmdb_5000_credits.csv",
    "https://raw.githubusercontent.com/carmengcm/TMDB_5000_Movie_Dataset_PythonAnalysis/master/tmdb_5000_credits.csv",
    "https://raw.githubusercontent.com/ReemAlsaedi/TMDb-5000-Movie-Dataset/master/tmdb_5000_credits.csv"
]
dest = r"c:\Users\poola\Downloads\Python Intern\Python_month_3\tmdb_5000_credits.csv"

def report_hook(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        s = f"\rDownloading credits CSV: {percent:.1f}% ({read_so_far / 1024 / 1024:.1f} MB of {total_size / 1024 / 1024:.1f} MB)"
        sys.stdout.write(s)
        sys.stdout.flush()
    else:
        sys.stdout.write(f"\rDownloading: {read_so_far / 1024 / 1024:.1f} MB")
        sys.stdout.flush()

download_success = False
for url in urls:
    print(f"Trying download from: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlretrieve(url, dest, reporthook=report_hook)
        print("\nDownload complete! File saved to:", dest)
        print("File size:", os.path.getsize(dest), "bytes")
        download_success = True
        break
    except Exception as e:
        print("\nDownload from this URL failed:", e)

if not download_success:
    print("\nAll download attempts failed.")
    sys.exit(1)
