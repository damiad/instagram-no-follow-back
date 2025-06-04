# Instagram Non-Follower Detector

This script helps you identify Instagram users you follow who do not follow you back. It's designed to work with the data export provided by Instagram.

## Features

- **Finds Non-Followers**: Compares your "following" list with your "followers" list to find who isn't following you back.
- **Sorts by Oldest Follow**: Displays the list of non-followers based on when you first followed them, from the oldest to the newest.
- **Configurable Tab Opening**: Automatically opens a specified number of profiles in Google Chrome for quick review.
- **Customizable Skipping**: Allows you to skip a certain number of the oldest accounts from being opened in tabs, so you can focus on more recent follows.

## Requirements

- **Python 3**: The script is written in Python 3. You can download it from [python.org](https://www.python.org/).
- **Google Chrome**: Required for the automatic tab-opening feature.

---

## Instructions

### Step 1: Download Your Instagram Data

First, you need to request your "Followers and following" data from Instagram.

**Using the Instagram App:**

1.  Go to your profile by tapping your profile picture in the bottom right.
2.  Tap the three horizontal lines (Menu) in the top right.
3.  Select **"Your activity"**.
4.  Tap **"Download your information"** and then **"Download or transfer information"**.
5.  Choose **"Some of your information"**.
6.  Select **"Followers and following"** and tap **"Next"**.
7.  Choose **"Download to device"** and tap **"Next"**.
8.  Select your desired date range (**"All time"** is recommended for a complete list) and make sure the format is set to **JSON**. Tap **"Save"**.

Instagram will compile your data and notify you via email and in the app when the download is ready. This can take some time.

### Step 2: Prepare Your Files

1.  Once your download is complete, download the `.zip` file from Instagram.
2.  Unzip the file. Inside, navigate to the `followers_and_following` folder.
3.  You will find the following files:
    - `following.json`
    - `followers_1.json`
    - `followers_2.json` (and possibly more, depending on your follower count)
4.  Place the `followers_and_following` folder in same directory as script (`non-follow-back-detector.py`).

Your folder should look something like this:

```
non-follow-back-detector.py
followers_and_following/
├── following.json
├── followers_1.json
├── followers_2.json
└── ... and so on
```

### Step 3: Configure the Script (Optional)

You can customize the script's behavior by editing these variables at the top of the file:

- `skip_oldest_followers`: The number of oldest non-followers to skip from being opened in browser tabs. They will still be listed in the terminal. (Default: `100`)
- `max_tabs_to_open`: The maximum number of profiles to open in Chrome after the skipped group. (Default: `35`)

### Step 4: Run the Script

1.  Open your Terminal (on macOS/Linux) or Command Prompt (on Windows).
2.  Navigate to the `instagram-no-follow-back` directory where your files are located.
    ```bash
    cd path/to/your/repository
    ```
3.  Run the script using Python 3:
    ```bash
    python3 non-follow-back-detector.py
    ```

The script will then process your files, print the complete sorted list of non-followers to the terminal, and open the specified profiles in new Chrome tabs.
