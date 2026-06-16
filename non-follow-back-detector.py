import json
import webbrowser
import time
import glob
import os
import re

# Config:
# Number of oldest non-followers to skip from opening in tabs
skip_oldest_followers = 0
    
# Maximum number of tabs to open in the browser
max_tabs_to_open = 37
# End Config

EXPORT_PATHS = [
    'connections/followers_and_following',
    'followers_and_following',
]

def find_export_directory():
    """Find the followers_and_following directory in old or new export layouts."""
    for export_path in EXPORT_PATHS:
        if os.path.isdir(export_path):
            return export_path
    return None

def username_from_string(value):
    """Extract a clean username from a value, href, or URL fragment."""
    if not value:
        return None

    s = str(value).strip()

    url_match = re.search(r'(?:https?://)?(?:www\.)?instagram\.com/(?:_u/)?([^/?#]+)', s, re.I)
    if url_match:
        s = url_match.group(1)

    if s.startswith('_u/'):
        s = s[3:]

    s = s.lstrip('@').rstrip('/')

    if not s or s in ('_u', 'www.instagram.com'):
        return None
    return s

def extract_username(entry):
    """Extract a username from a string_list_data entry."""
    for candidate in (entry.get('value'), entry.get('username'), entry.get('href')):
        username = username_from_string(candidate)
        if username:
            return username
    return None

def profile_url(username):
    """Build an Instagram profile URL using the /_u/ path."""
    return f"https://www.instagram.com/_u/{username}"

def get_relationship_list(data):
    """Return the list of relationship entries from old or new JSON formats."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in (
            'relationships_following',
            'relationships_followers',
            'relationships_follow_requests_sent',
        ):
            if isinstance(data.get(key), list):
                return data[key]
        for value in data.values():
            if isinstance(value, list):
                return value
    return []

def get_user_data_from_file(file_path):
    """
    Reads a JSON file and extracts a dictionary of usernames and timestamps.
    """
    user_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data_list = get_relationship_list(data)

            for item in data_list:
                for entry in item.get("string_list_data", []):
                    username = extract_username(entry)
                    if username:
                        user_data[username] = entry.get("timestamp", 0)
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}. Skipping.")
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {file_path}. The file might be empty or corrupt.")
    except Exception as e:
        print(f"An unexpected error occurred with {file_path}: {e}")
        
    return user_data

def main():
    """
    Main function to find users you follow who don't follow you back.
    """
    followers_and_following_path = find_export_directory()
    if not followers_and_following_path:
        print("Error: Could not find your Instagram export data.")
        print("Place the export folder at one of these locations:")
        for export_path in EXPORT_PATHS:
            print(f"  - {export_path}/")
        return

    following_files = sorted(glob.glob(os.path.join(followers_and_following_path, 'following*.json')))
    follower_files = sorted(glob.glob(os.path.join(followers_and_following_path, 'followers_*.json')))

    if not following_files:
        print(f"Error: No following file found in '{followers_and_following_path}'.")
        print("Expected following.json or following_1.json.")
        return

    if not follower_files:
        print(f"Error: No follower files found in '{followers_and_following_path}'.")
        print("Expected followers_1.json, followers_2.json, etc.")
        return

    print(f"Using export directory: {followers_and_following_path}")
    print(f"Found {len(follower_files)} follower file(s) to process.")

    print("\nProcessing your 'following' list...")
    following_data = {}
    for following_file in following_files:
        following_data.update(get_user_data_from_file(following_file))
    if following_data:
        print(f"Found {len(following_data)} accounts you are following.")

    followers = set()
    print("\nProcessing your 'followers' lists...")
    for follower_file in follower_files:
        followers.update(get_user_data_from_file(follower_file).keys())
        
    if followers:
        print(f"Found a total of {len(followers)} followers.")

    if following_data and followers:
        not_following_back_usernames = following_data.keys() - followers
        
        not_following_back_list = [
            (username, following_data[username]) 
            for username in not_following_back_usernames
        ]
        
        sorted_list = sorted(not_following_back_list, key=lambda item: item[1])

        print(f"\n--- {len(sorted_list)} Users Who Don't Follow You Back (sorted oldest to newest) ---")
        print(f"Skipping the first {skip_oldest_followers} users from being opened in tabs.")

        browser = None
        
        try:
            browser = webbrowser.get('chrome')
            list_for_tabs = sorted_list[skip_oldest_followers:]
            print(f"Will attempt to open the next {min(len(list_for_tabs), max_tabs_to_open)} profiles in Chrome...")
        except webbrowser.Error:
            print("Could not find Google Chrome. Printing all links to the console instead.")
        
        tabs_opened = 0
        for i, (username, timestamp) in enumerate(sorted_list):
            url = profile_url(username)

            if i < skip_oldest_followers:
                print(url)
            elif browser and tabs_opened < max_tabs_to_open:
                browser.open_new_tab(url)
                print(f"Opening tab ({tabs_opened + 1}/{max_tabs_to_open}): {url}")
                tabs_opened += 1
                time.sleep(0.1)
            else:
                print(url)
    else:
        print("\nCould not perform the comparison due to missing data.")


if __name__ == "__main__":
    main()
