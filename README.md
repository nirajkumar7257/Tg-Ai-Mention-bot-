<h1 align="center"><b>🤖 Tg AI Mention Bot</b></h1>

<h4 align="center">
  <b>Telegram Group AI-Powered Tagging & Mention Bot</b><br>
  <sub>Powered by Google Gemini AI • Built with Python • Deployed on Heroku</sub>
</h4>

<p align="center">
  <a href="https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python&logoColor=white">
  </a>
  <a href="https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram">
  </a>
  <a href="https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square">
  </a>
  <a href="https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/github/stars/nirajkumar7257/Tg-Ai-Mention-bot-?style=flat-square">
  </a>
</p>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Deploy](#-quick-deploy)
- [📥 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [📖 Commands](#-commands)
- [🛠️ Setup Guide](#️-setup-guide)
- [💡 Usage Examples](#-usage-examples)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)
- [📜 License](#-license)

---

## ✨ Features

### 🎯 Core Features
- ✅ **AI-Powered Responses** - Google Gemini AI integration for smart replies
- ✅ **Mass Tagging** - Tag all members or admins in one command
- ✅ **Multiple Tagging Styles** - Hindi, English, Jokes, Good Morning/Night messages
- ✅ **Voice Chat Detection** - Special VC invite tag for online members
- ✅ **Admin Controls** - Pause, Resume, Stop tagging commands
- ✅ **User-Friendly** - Simple commands, easy to use

### 🔐 Security & Reliability
- ✅ **Rate Limiting** - Prevents spam and abuse
- ✅ **Admin-Only Commands** - Protected tagging operations
- ✅ **Error Handling** - Graceful error management
- ✅ **Async Processing** - Non-blocking operations

### 📊 Analytics & Monitoring
- ✅ **Usage Statistics** - Track bot activity
- ✅ **Broadcast Capability** - Send messages to all groups
- ✅ **Owner Commands** - Full control for bot owner

---

## 🚀 Quick Deploy

### Deploy to Heroku (One-Click)

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-black?style=for-the-badge&logo=heroku" alt="Deploy to Heroku">
  </a>
</p>

**What You'll Need:**
1. Telegram Bot Token from [@BotFather](https://t.me/BotFather)
2. Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Your Telegram User ID (from [@userinfobot](https://t.me/userinfobot))
4. Heroku Account

---

## 📥 Installation

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Telegram Bot Token
- Gemini API Key

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-
   cd Tg-Ai-Mention-bot-
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your tokens
   ```

5. **Run the Bot**
   ```bash
   python bot.py
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Telegram Bot Token from @BotFather
TELEGRAM_TOKEN=your_bot_token_here

# Google Gemini API Key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_key_here

# Your Telegram User ID (numeric, get from @userinfobot)
OWNER_ID=your_user_id_here

# Heroku App Name (without https://)
HEROKU_APP_NAME=your-heroku-app-name

# Support Channel Link (optional)
SUPPORT_LINK=https://t.me/your_channel_name

# Server Port (usually 8443 for Heroku)
PORT=8443
```

### How to Get Tokens

#### 🤖 Telegram Bot Token
1. Open [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow the instructions and get your token

#### 🧠 Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your free API key

#### 👤 Your User ID
1. Open [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send any message
3. Copy your numeric User ID

---

## 📖 Commands

### 🏷️ Tagging Commands (Admin Only)

| Command | Description | Style |
|---------|-------------|-------|
| `/hitag` | Tag all members in Hindi | 🇮🇳 Hindi |
| `/entag` | Tag all members in English | 🇬🇧 English |
| `/gmtag` | Good Morning greeting (Hinglish) | 🌅 Morning |
| `/gntag` | Good Night greeting (Hinglish) | 🌙 Night |
| `/tagall` | General tag all members | 🔥 All |
| `/jtag` | Funny joke tagging | 😂 Jokes |
| `/vctag` | Voice Chat invite (online members first) | 🎙️ VC |

### 👥 Mention Commands (Everyone)

| Command | Description |
|---------|-------------|
| `/admin` or `@admin` | Tag all admins (6 per message) |
| `/all` or `@all` | Tag all members (6 per message) |

**With Custom Messages:**
```
/admin please join voice chat
/all meeting in 5 mins
```

### 🎮 Control Commands (Admin Only)

| Command | Description |
|---------|-------------|
| `/stop` | Stop ongoing tagging process |
| `/pause` | Pause tagging temporarily |
| `/resume` | Resume paused tagging |

### 👑 Owner Commands (Owner Only)

| Command | Description |
|---------|-------------|
| `/broadcast <message>` | Broadcast message to all groups |
| `/stats` | View bot usage statistics |

---

## 🛠️ Setup Guide

### Step 1: Get Requirements

- [ ] Telegram Bot Token (from @BotFather)
- [ ] Gemini API Key (from aistudio.google.com)
- [ ] Your Telegram User ID (from @userinfobot)
- [ ] Heroku Account (heroku.com)

### Step 2: Deploy Options

#### Option A: One-Click Heroku Deploy (Recommended)

1. Click the Heroku deploy button above
2. Fill in the environment variables
3. Click "Deploy App"
4. Bot will be live in 2-3 minutes

#### Option B: Manual Heroku Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_key
heroku config:set OWNER_ID=your_id
heroku config:set HEROKU_APP_NAME=your-app-name

# Deploy
git push heroku main
```

#### Option C: Local Development

1. Clone repository
2. Set up virtual environment
3. Install dependencies
4. Configure `.env` file
5. Run `python bot.py`

### Step 3: Add Bot to Group

1. Find your bot username on [@BotFather](https://t.me/BotFather)
2. Open the bot and click "Start"
3. Add bot to your Telegram group
4. Make bot an admin with message permissions
5. Start using commands!

---

## 💡 Usage Examples

### Example 1: Tag All Members in Hindi
```
/hitag
```
**Output:** नमस्ते @user1 @user2 @user3 ... (all members tagged)

### Example 2: Good Morning Tag
```
/gmtag
```
**Output:** Good Morning everyone! ☀️ @user1 @user2 @user3 ...

### Example 3: Voice Chat Invite
```
/vctag
```
**Output:** Join VC 🎙️ @user1 @user2 (online members prioritized)

### Example 4: Custom Mention
```
/admin please check the announcement
```
**Output:** @admin1 @admin2 please check the announcement

### Example 5: View Statistics
```
/stats
```
**Output:** Shows bot usage in your group

---

## 🔄 Project Structure

```
Tg-Ai-Mention-bot-/
├── bot.py              # Main bot logic
├── app.json            # Heroku configuration
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version
├── Procfile           # Heroku process file
├── .env.example       # Environment template
├── README.md          # This file
└── LICENSE            # MIT License
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-
   cd Tg-Ai-Mention-bot-
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes and Commit**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**
   - Describe your changes clearly
   - Link any related issues

---

## 📞 Support

### Need Help?

- **Telegram Channel:** [@Comeback_009](https://t.me/Comeback_009)
- **Telegram Group:** [Join Support Group](https://t.me/your_support_group)
- **GitHub Issues:** [Report Issues](https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-/issues)

### Common Issues

**Q: Bot is not responding**
- Check if bot is added to group as admin
- Verify bot token in `.env`
- Check bot has message permissions

**Q: Tagging not working**
- Ensure you're an admin in the group
- Check if bot has admin permissions
- Verify group has 10+ members

**Q: Heroku deployment failed**
- Check all environment variables are set
- Verify tokens are correct
- Check Heroku dyno logs

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Niraj Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Credits

- **Developer:** [Comeback](https://t.me/comeback_009)
- **AI Engine:** Google Gemini AI
- **Bot Framework:** python-telegram-bot
- **Hosting:** Heroku

---

## 📈 Roadmap

- [ ] Database integration for better analytics
- [ ] Custom message scheduling
- [ ] Multi-language support
- [ ] Web dashboard for statistics
- [ ] Advanced filtering options

---

<p align="center">
  <b>Made with ❤️ by Niraj Kumar</b><br>
  <a href="https://github.com/nirajkumar7257">Visit My GitHub</a> • 
  <a href="https://t.me/comeback_009">Contact Me</a>
</p>

<p align="center">
  <a href="https://github.com/nirajkumar7257/Tg-Ai-Mention-bot-">
    <img src="https://img.shields.io/badge/⭐_If_you_found_this_useful_please_star_it-white?style=for-the-badge">
  </a>
</p>
