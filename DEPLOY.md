# Deployment Guide

## Vercel (Recommended - Serverless)

The bot is currently deployed on Vercel using webhook mode.

### Quick Deploy

1. Fork or clone the repo
2. Run `npx vercel --prod --yes`
3. Add BOT_TOKEN: `npx vercel env add BOT_TOKEN production`
4. Redeploy: `npx vercel --prod --yes`
5. Set webhook: `curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-app.vercel.app/api/webhook"`

### Verify Deployment

```bash
# Check webhook status
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Check endpoint is live
curl "https://your-app.vercel.app/api/webhook"
```

### Adding Persistence (Optional)

For user data to persist between function invocations:

1. Create free Upstash Redis database at https://upstash.com
2. Add environment variables:
   - `UPSTASH_REST_URL`
   - `UPSTASH_REST_TOKEN`
3. Redeploy

## Railway (Alternative - Always-on)

Use the original `bot.py` with polling mode:

```bash
railway init
railway add --database postgresql  # if needed
railway variables set BOT_TOKEN=your_token
railway up
```

## Local Development

```bash
export BOT_TOKEN=your_token
python bot.py  # Uses polling mode
```
