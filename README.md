# SnapTaskBot

SnapTaskBot is a Telegram bot designed to manage photography tasks in a channel. Administrators can add new themes, start polls, set weekly themes, and more.

## Getting Started

Follow the instructions below to install and set up SnapTaskBot on your device.

### Prerequisites

- Python 3.9+
- A created bot in Telegram and an API token obtained from BotFather

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/SnapTaskBot.git
   cd SnapTaskBot
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # For Windows: myenv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your environment variables:

   ```plaintext
   TELEGRAM_TOKEN=your-telegram-bot-token
   SECRET_PHRASE=your-sercret-phrase
   ```

5. Create a `data` folder in the project root and create a `channel_data.json` file:

   ```bash
   mkdir data
   echo "{}" > data/channel_data.json
   ```

### Running the Bot

Run the bot with the following command:

```bash
python bot.py
```

## Usage

Administrators can use the following commands in private messages with the bot:

- `/authorize <secret_phrase> <channel_id>` - Authorize a channel admin in the bot.
- `/addtheme <theme>` - Add a new theme to the channel's theme list.
- `/startvote` - Start a poll with 4 random themes.
- `/endvote` - End the poll and set the theme with the most votes as the weekly theme.
- `/newtheme` - Randomly select a weekly theme and set it as the current theme.
- `/showtheme` - Display the current weekly theme in the channel.
- `/themes` - Show a list of all themes.

### Example Commands

1. **Authorization:**
   ```plaintext
   /authorize thereisnospoon -1001234567890
   ```

2. **Adding a Theme:**
   ```plaintext
   /addtheme Morning mist
   ```

3. **Starting a Poll:**
   ```plaintext
   /startvote
   ```

4. **Ending a Poll:**
   ```plaintext
   /endvote
   ```

5. **Setting a New Weekly Theme:**
   ```plaintext
   /newtheme
   ```

6. **Showing the Current Weekly Theme:**
   ```plaintext
   /showtheme
   ```

7. **Showing All Available Themes:**
   ```plaintext
   /themes
   ```

## Contributing

If you would like to contribute to the project, please follow the standard GitHub workflow: fork, change, PR.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please create issue.