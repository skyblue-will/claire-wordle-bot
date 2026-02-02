# 🎮 Claire's Wordle Bot

A Telegram Wordle game bot built for Claire! More addictive than the original.

**Bot:** [@WillPipBot](https://t.me/WillPipBot)

## Features

- 📅 **Daily Puzzle** - Same word for everyone, changes daily
- 🎯 **Practice Mode** - Unlimited games to sharpen your skills
- 🔥 **Streaks** - Track your daily winning streak
- 📊 **Statistics** - Games played, win rate, guess distribution
- 💡 **Hints** - Get letter reveals (costs 1 streak point!)
- 📋 **Share Results** - Shareable emoji grids

## Commands

- `/start` - Welcome message and instructions
- `/play` - Start today's daily puzzle
- `/practice` - Start an unlimited practice game
- `/quit` - Give up on current practice game
- `/stats` - View your statistics
- `/hint` - Get a hint (costs streak in daily mode)

## How to Play

1. Guess a 5-letter word
2. Get feedback:
   - 🟩 = Correct letter, correct position
   - 🟨 = Correct letter, wrong position
   - ⬛ = Letter not in word
3. Solve in 6 tries!

## Deployment

### Vercel (Current)

The bot runs as a serverless function on Vercel with webhook mode.

**Live URL:** https://claire-wordle-bot.vercel.app

**Deploy your own:**
```bash
# Clone the repo
git clone https://github.com/skyblue-will/claire-wordle-bot

# Deploy to Vercel
npx vercel --prod --yes

# Set the bot token
npx vercel env add BOT_TOKEN production

# Redeploy to pick up env var
npx vercel --prod --yes

# Set webhook with Telegram
curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-project.vercel.app/api/webhook"
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `UPSTASH_REST_URL` | (Optional) Upstash Redis URL for persistence |
| `UPSTASH_REST_TOKEN` | (Optional) Upstash Redis token |

### Data Persistence

Currently, user data persists within a single function invocation. For production use with persistent data:

1. Create a free [Upstash Redis](https://upstash.com/) database
2. Add `UPSTASH_REST_URL` and `UPSTASH_REST_TOKEN` to Vercel environment variables
3. Redeploy

## Built With

- Python 3.12
- Vercel Serverless Functions
- Telegram Bot API

---

Built with 💜 by Pip for Claire
