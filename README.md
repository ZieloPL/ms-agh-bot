# MS AGH DSNet Facility Reservation Bot

This Python script, **utilizing the Selenium library for browser automation,** automates the process of booking facilities (Football Pitch or AV Room) on the AGH DSNet student portal (`panel.dsnet.agh.edu.pl`). It is designed to make reservations precisely when they become available (the "drop time"), increasing the chances of securing a slot.

## Features

*   **Automated Login:** Logs into the DSNet panel using credentials from a `.env` file.
*   **Facility Selection:** Allows users to choose between Football Pitch and AV Room.
*   **Time-Slot Specification:** Users can specify the desired day, month, start, and end times for the reservation.
*   **Dual Booking (AV Room):** Supports booking one or two consecutive hour-long slots for the AV Room.
*   **Precise Timing:**
    *   Synchronizes with an external time API (`timeapi.io`) to get an accurate current time.
    *   Calculates the exact moment to refresh the page and attempt the reservation.
    *   Includes a "busy-wait" loop for sub-second precision leading up to the drop time.
*   **Automated Navigation:** Clicks through the necessary links to reach the reservation page for the selected facility.
*   **Targeted Reservation Click:** Identifies and clicks the correct "reserve" button based on the specified time slot.

## How it Works

1.  **User Input:** The script prompts the user for reservation details (day, month, facility, desired time slots).
2.  **Credentials:** It loads login credentials from a `.env` file.
3.  **Time Synchronization:** It fetches the current time from `timeapi.io` and calculates an offset with the local system time. This ensures actions are triggered based on a more universally accurate time.
4.  **Target Time Calculation:** A target timestamp is set for 06:01 (Football) or 21:01 (AV Room) on the specified drop day/month.
5.  **Login & Navigation:** The script uses Selenium to open a Chrome browser, log into the DSNet panel, and navigate to the relevant facility's reservation page.
6.  **Waiting Loop:** It enters a loop, continuously checking the synchronized time against the target drop time.
    *   If far from the drop time, it sleeps for longer random intervals and refreshes the page periodically to keep the session alive.
    *   As the drop time approaches, sleep intervals become very short (milliseconds) for precision.
7.  **Reservation Attempt:** Once the target time is reached:
    *   The page is refreshed to load the newly available slots.
    *   The `res()` function is called, which scans the reservation table for the user-specified time slot and clicks the corresponding "reserve" button.
    *   If booking two slots (for AV Room), the page is refreshed again, and `res()` is called for the second slot.
8.  **Completion:** The script waits for user input (Enter key) before closing the browser.

## Prerequisites

*   Python 3.x
*   Google Chrome browser
*   ChromeDriver (compatible with your Google Chrome version)

## Setup

1.  **Clone the repository (or download the script):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install selenium requests python-dotenv
    ```

3.  **Download and set up ChromeDriver:**
    *   Check your Google Chrome version (e.g., `chrome://settings/help`).
    *   Download the corresponding ChromeDriver from [ChromeDriver - WebDriver for Chrome](https://googlechromelabs.github.io/chrome-for-testing/).
    *   Place `chromedriver.exe` (or `chromedriver` on Linux/macOS) in a known location.
    *   **Update the path to ChromeDriver in the script:**
        Modify the line:
        ```python
        service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
        ```
        to point to your `chromedriver.exe` location, e.g., `service = Service(r"C:\path\to\your\chromedriver.exe")` or `service = Service("/usr/local/bin/chromedriver")`.

4.  **Create a `.env` file:**
    In the same directory as the script, create a file named `.env` with your DSNet login credentials:
    ```env
    MSAGH_EMAIL="your_email@student.agh.edu.pl"
    MSAGH_PASSWORD="your_password"
    ```
    Replace `your_email@student.agh.edu.pl` and `your_password` with your actual credentials.

## Usage

1.  Follow the on-screen prompts:
    *   **Enter the drop day:** (e.g., `15`)
    *   **Enter the drop month:** (e.g., `7` for July)
    *   **Choose your facility:**
        *   `1` for Football Pitch
        *   `2` for AV Room
    *   **If AV Room, how many hours?** (`1` or `2`)
    *   **Enter starting hour of your reservation (hh:mm):** (e.g., `18:00`)
    *   **Enter ending hour of your reservation (hh:mm):** (e.g., `19:00`)
    *   If booking a second hour for AV Room, you'll be prompted for its start and end times as well.

2.  The script will then proceed to log in, navigate, and wait for the calculated drop time.
3.  A Chrome browser window will open and be controlled by the script. Do not close it manually unless you want to stop the script.

## Important Notes

*   **Use Responsibly:** This script automates interaction with a live system. Ensure you are using it in accordance with any terms of service of the DSNet panel.
*   **Website Changes:** The script relies on specific HTML structures (element IDs, class names, CSS selectors, link `href` attributes). If the DSNet website is updated, the script may break and require updates.
    *   Notably, facility IDs like `2192` (Football) and `2380` (AV Room) are hardcoded in the navigation links.
*   **Drop Times:** The script assumes specific drop times:
    *   Football Pitch: 06:01 AM
    *   AV Room: 21:01 (9:01 PM)
    These are hardcoded (`hour = 6 if facility == 1 else 21`, `minute = 1`). If these change, the script needs to be updated.
*   **Error Handling:** Basic error handling is in place (e.g., "Not this time..." if a reservation button isn't found). More robust error handling could be added.
*   **Zoom Level:** The script sets the browser zoom to 50% (`driver.execute_script("document.body.style.zoom='50%'")`) before attempting to find reservation buttons. This is likely to ensure consistent element visibility and interaction.
*   **Network Latency:** While the script syncs with an external time API, network latency can still play a minor role.

## Disclaimer

This script is provided as-is. The user assumes all responsibility for its use. The author is not responsible for any missed reservations, account issues, or any other consequences arising from the use of this script.
