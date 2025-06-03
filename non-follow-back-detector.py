import json
import webbrowser
import time

def get_user_data_from_file(file_path, key):
    """
    Reads a JSON file and extracts a dictionary of usernames and timestamps.

    Args:
        file_path (str): The path to the JSON file.
        key (str): The top-level key in the JSON file 
                   (e.g., 'relationships_following').

    Returns:
        dict: A dictionary mapping usernames to their timestamps.
    """
    user_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # The structure for followers is a simple list of objects,
            # while for following it's nested under a key.
            if isinstance(data, dict):
                data_list = data.get(key, [])
            else:
                data_list = data

            for item in data_list:
                for entry in item.get("string_list_data", []):
                    # Store username and its corresponding timestamp
                    user_data[entry.get("value")] = entry.get("timestamp", 0)
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
    # --- Configuration ---
    # Path to your 'following.json' file
    following_file = 'following.json'
    
    # List of your follower data files
    follower_files = [f'followers_{i}.json' for i in range(1, 6)]

    # Number of oldest non-followers to skip from opening in tabs
    skip_oldest_followers = 30
    
    # Maximum number of tabs to open in the browser
    max_tabs_to_open = 35
    # --- End Configuration ---

    # Get the dictionary of users you are following with their timestamps
    print("Processing your 'following' list...")
    following_data = get_user_data_from_file(following_file, 'relationships_following')
    if following_data:
        print(f"Found {len(following_data)} accounts you are following.")

    # Combine all followers from the different follower files into a set
    followers = set()
    print("\nProcessing your 'followers' lists...")
    for follower_file in follower_files:
        # We only need the usernames (keys) from the follower files
        followers.update(get_user_data_from_file(follower_file, '').keys())
        
    if followers:
        print(f"Found a total of {len(followers)} followers.")

    # Find the users who are in your 'following' list but not in your 'followers' list
    if following_data and followers:
        # Get the usernames of those who don't follow back
        not_following_back_usernames = following_data.keys() - followers
        
        # Create a list of tuples (username, timestamp) for sorting
        not_following_back_list = [
            (username, following_data[username]) 
            for username in not_following_back_usernames
        ]
        
        # Sort the list by timestamp (the second element in the tuple), from oldest to newest
        sorted_list = sorted(not_following_back_list, key=lambda item: item[1])

        print(f"\n--- {len(sorted_list)} Users Who Don't Follow You Back (sorted oldest to newest) ---")
        print(f"Skipping the first {skip_oldest_followers} users from being opened in tabs.")

        browser = None
        
        # Try to get the Google Chrome browser controller.
        try:
            browser = webbrowser.get('chrome')
            list_for_tabs = sorted_list[skip_oldest_followers:]
            print(f"Will attempt to open the next {min(len(list_for_tabs), max_tabs_to_open)} profiles in Chrome...")
        except webbrowser.Error:
            print("Could not find Google Chrome. Printing all links to the console instead.")
        
        tabs_opened = 0
        for i, (username, timestamp) in enumerate(sorted_list):
            url = f"https://www.instagram.com/{username}"

            # Check if the user is in the group to be skipped from tab opening
            if i < skip_oldest_followers:
                print(url)
            # If not in the skip group, check if we should open a tab
            elif browser and tabs_opened < max_tabs_to_open:
                browser.open_new_tab(url)
                print(f"Opening tab ({tabs_opened + 1}/{max_tabs_to_open}): {url}")
                tabs_opened += 1
                # Add a small delay to prevent overwhelming the browser
                time.sleep(0.1)
            else:
                # Otherwise (no browser, or max tabs reached), just print the URL
                print(url)
    else:
        print("\nCould not perform the comparison due to missing data.")


if __name__ == "__main__":
    main()
