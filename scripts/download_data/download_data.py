import os
import subprocess

def download_data():
    os.makedirs("../../data/raw", exist_ok=True)

    dataset_id = "parksung98/healthcare-provider-claims"

    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", dataset_id,
        "-p", "data/raw",
        "--unzip"
    ], check=True)

    print("Download completed.")

def main():
    download_data()

if __name__ == "__main__":
    main()