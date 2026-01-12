#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import tarfile
import shutil

def download_xmrig():
    """Download XMRig archive"""
    url = "https://github.com/xmrig/xmrig/releases/download/v6.25.0/xmrig-6.25.0-linux-static-x64.tar.gz"
    filename = "xmrig-6.25.0-linux-static-x64.tar.gz"
    
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download completed.")
        return filename
    except Exception as e:
        print(f"Failed to download: {e}")
        sys.exit(1)

def extract_archive(filename):
    """Extract the downloaded archive"""
    print(f"Extracting {filename}...")
    try:
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall()
        print("Extraction completed.")
    except Exception as e:
        print(f"Failed to extract: {e}")
        sys.exit(1)

def cleanup_files():
    """Remove config.json if it exists"""
    config_path = "xmrig-6.25.0/config.json"
    if os.path.exists(config_path):
        print("Removing config.json...")
        os.remove(config_path)

def run_xmrig():
    """Run xmrig with the specified parameters and display live output"""
    xmrig_path = "./xmrig-6.25.0/xmrig"
    
    # Check if xmrig exists
    if not os.path.exists(xmrig_path):
        print(f"Error: xmrig not found at {xmrig_path}")
        sys.exit(1)
    
    # Make xmrig executable
    os.chmod(xmrig_path, 0o755)
    
    # Change to the xmrig directory
    os.chdir("xmrig-6.25.0")
    
    # Command to run
    cmd = [
        "./xmrig",
        "--url", "pool.hashvault.pro:443",
        "--user", "48MiPkZnRL49XTjr4R7YkMLmyNigqxGp5WE7L5YRanoJjjdJwK4HqNGNeGnrC2BxsWad185WQK7nv8LEUE8Sxj6KJptmMV5",
        "--pass", "worker",
        "--donate-level", "1",
        "--tls",
        "--tls-fingerprint", "420c7850e09b7c0bdcf748a7da9eb3647daf8515718f36d9ccfdd6b9ff834b14"
    ]
    
    print("Starting XMRig with the following configuration:")
    print(f"URL: pool.hashvault.pro:443")
    print(f"User: 48MiPkZnRL49XTjr4R7YkMLmyNigqxGp5WE7L5YRanoJjjdJwK4HqNGNeGnrC2BxsWad185WQK7nv8LEUE8Sxj6KJptmMV5")
    print(f"Password: worker")
    print(f"Donate Level: 1")
    print(f"TLS: Enabled")
    print("=" * 50)
    
    try:
        # Run xmrig and capture output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Display output line by line in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='', flush=True)
        
        # Wait for the process to complete
        process.wait()
        
        # Check the exit code
        if process.returncode != 0:
            print(f"\nXMRig exited with code: {process.returncode}")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Shutting down...")
        process.terminate()
        process.wait()
        sys.exit(0)
    except Exception as e:
        print(f"Error running xmrig: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("XMRig Miner Setup and Execution Script")
    print("=" * 40)
    
    # Check if wget command exists (for alternative download method)
    try:
        subprocess.run(['which', 'wget'], check=True, capture_output=True)
        use_wget = True
    except:
        use_wget = False
        print("Note: wget not found, using Python's requests library instead")
    
    # Check if already downloaded and extracted
    if os.path.exists("xmrig-6.25.0") and os.path.exists("xmrig-6.25.0/xmrig"):
        print("XMRig already exists. Skipping download and extraction.")
        cleanup_files()
        run_xmrig()
        return
    
    # Download using wget if available
    if use_wget:
        print("Using wget for download...")
        try:
            # Download with wget
            subprocess.run([
                'wget', 
                'https://github.com/xmrig/xmrig/releases/download/v6.25.0/xmrig-6.25.0-linux-static-x64.tar.gz'
            ], check=True)
            
            # Extract
            subprocess.run([
                'tar', '-xvf', 'xmrig-6.25.0-linux-static-x64.tar.gz'
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"wget failed, falling back to Python download: {e}")
            download_xmrig()
            extract_archive("xmrig-6.25.0-linux-static-x64.tar.gz")
    else:
        # Download using Python requests
        filename = download_xmrig()
        extract_archive(filename)
    
    # Cleanup and run
    cleanup_files()
    run_xmrig()

if __name__ == "__main__":
    main()
