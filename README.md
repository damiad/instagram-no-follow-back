# Instagram Non-Follower Detector

A web-based tool to help you identify Instagram users you follow who do not follow you back. This tool runs entirely in your browser—your data is never uploaded to any server, ensuring your privacy.

**Live Tool**: [**https://damiad.github.io/instagram-no-follow-back/**](https://damiad.github.io/instagram-no-follow-back/)

## Features

-   **Web-Based Interface**: No installation required. Just open the link and upload your data.
-   **Privacy Focused**: All processing is done client-side in your browser. Your files are never sent to a server.
-   **Flexible Uploads**: Works with both the `.zip` file from Instagram and an unzipped directory.
-   **Sorted Results**: Displays the list of non-followers based on when you first followed them, from oldest to newest.
-   **Bulk Profile Opening**: Opens multiple profiles in new tabs at once to make reviewing them easy.
-   **Customizable**: Set how many of the oldest accounts to skip and the maximum number of tabs to open.

---

## How to Use (Web UI - Recommended)

### Step 1: Download Your Instagram Data

First, you need to request your "Followers and following" data from Instagram.

1.  On the Instagram app or website, go to your profile.
2.  Navigate to **Menu** > **Your activity**.
3.  Select **Download your information** > **Download or transfer information**.
4.  Choose **Some of your information**.
5.  Select only **"Followers and following"** and tap **Next**.
6.  Choose **Download to device** and tap **Next**.
7.  Set the format to **JSON** and the date range to **All time**. Tap **Save**.

Instagram will notify you when your `.zip` file is ready to download.

### Step 2: Use the Web Tool

1.  Go to the live tool: [**https://damiad.github.io/instagram-no-follow-back/**](https://damiad.github.io/instagram-no-follow-back/)
2.  Upload your data using one of the two options:
    -   **Option A (Recommended):** Upload the entire `.zip` file you downloaded from Instagram.
    -   **Option B:** If you unzipped the file, upload the parent directory (e.g., `connections`).
3.  Adjust the "Skip Oldest" and "Max Tabs" parameters if needed.
4.  Click the **Find Non-Followers** button.

### Step 3: Review the Results

The tool will display a sorted list of users who don't follow you back.

> **IMPORTANT: Enable Pop-ups!**
> When you click the **"Open Profiles in New Tabs"** button, your browser will likely block the pop-ups initially. **Look for a pop-up blocked icon** in your browser's address bar. Click it and choose **"Always allow pop-ups and redirects from..."** for the site to work correctly.

---

## Alternative Method (Python Script)

For users who prefer a command-line interface, the original Python script is still available in the repository.

### Requirements

-   **Python 3**: Download from [python.org](https://www.python.org/).

### Instructions

1.  Download your Instagram data as described in Step 1 above and unzip it.
2.  Place the `followers_and_following` directory inside the project folder.
3.  Run the script from your terminal:
    ```bash
    python3 non-follow-back-detector.py
    ```

---

## Creator

Created by **[dadabrowski](https://www.instagram.com/dadabrowski/)**.

View the code and contribute on **[GitHub](https://github.com/damiad/instagram-no-follow-back)**.
