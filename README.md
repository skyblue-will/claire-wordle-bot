# Claire's Wordle Bot 🎮

A Telegram Wordle clone that's MORE addictive than the original. Built with love for Claire.

## Features

- 📅 **Daily Puzzle** - Same word for everyone, new word each day
- 🎯 **Practice Mode** - Unlimited games to sharpen your skills
- 🔥 **Streaks** - Track your daily solving streak (don't break it!)
- 📊 **Statistics** - Games played, win %, guess distribution
- 📋 **Shareable Results** - Copy-paste your emoji grid
- 💡 **Hints** - Get help, but it costs a streak point!

## Commands

- `/start` - Welcome message and how to play
- `/play` - Start today's daily puzzle
- `/practice` - Start an unlimited practice game
- `/stats` - View your statistics
- `/hint` - Get a hint (costs 1 streak point for daily!)
- `/quit` - Give up on practice game

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Deploy to Railway:
   ```bash
   railway login
   railway init
   railway up
   railway variables set BOT_TOKEN=your_token_here
   ```

## Game Mechanics

- Guess the 5-letter word in 6 tries
- 🟩 Green = Right letter, right position
- 🟨 Yellow = Right letter, wrong position
- ⬛ Gray = Letter not in word

## The Addictive Hooks

- **Streak anxiety** - Don't break that chain!
- **One more game** - Practice mode after daily
- **Hint cost** - Spend streak points for help (risky!)
- **Statistics** - Watch those numbers grow

---
Built by Pip for Claire 💜
