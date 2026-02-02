# Deployment Instructions

## Step 1: Create Telegram Bot

1. Open Telegram, search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name: `Claire's Wordle` (or anything)
4. Choose a username: Must end in `bot`, e.g. `clairewordle_bot`
5. Copy the token (looks like `123456:ABC-DEF...`)

## Step 2: Deploy to Railway

### Option A: Railway Dashboard (Easiest)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `skyblue-will/claire-wordle-bot`
4. Add environment variable:
   - `BOT_TOKEN` = your token from BotFather
5. Click Deploy!

### Option B: Railway CLI

```bash
cd /home/clawdbot/repos/claire-wordle-bot
railway login
railway init
railway up
railway variables set BOT_TOKEN=your_token_here
```

## Step 3: Test It!

Open your bot in Telegram and send `/start`

## Troubleshooting

- Check logs: `railway logs` or Railway dashboard
- Make sure BOT_TOKEN is set correctly
- Redeploy if needed: `railway up`

---

Bot URL: https://t.me/YOUR_BOT_USERNAME
