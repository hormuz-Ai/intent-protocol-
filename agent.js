const { Configuration, OpenAIApi } = require('openai');
const { Client } = require('@anthropic-ai/sdk');
const nodemailer = require('nodemailer');
const TelegramBot = require('node-telegram-bot-api');
const cron = require('node-cron');
const fs = require('fs');
const path = require('path');

// ========== CONFIG ==========
const CONFIG = {
  keys: {
    gemini: 'AIzaSyDiK57d7ReTzNYMlsr20oMEHrwaQZIYG74',
    // Add Claude or OpenAI keys if needed later
  },
  email: {
    user: 'jarvis.intp@gmail.com',      // Your Jarvis email (KeyID or Gmail)
    pass: 'YOUR_APP_PASSWORD',           // Gmail App Password
    investorAlias: 'investors@intentprotocol.org'
  },
  telegram: {
    token: 'YOUR_TELEGRAM_BOT_TOKEN',
    founderChatId: 'YOUR_TELEGRAM_CHAT_ID'
  },
  wallet: {
    address: '6iewCKAoERKRQHAQjbfQd2pmGPrK3HE4y8L4p8kWrQoU',
    chain: 'solana'
  },
  litepaperUrl: 'https://github.com/Hormuz-Ai/intent-protocol-/blob/main/LITEPAPER.md',
  githubUrl: 'https://github.com/Hormuz-Ai/intent-protocol-',
  demoUrl: 'https://x.com/i/status/2048104459415224426',
  calendlyUrl: 'https://calendly.com/zundesaviours6',
  discordInvite: 'https://discord.gg/3v8Ft5Y8f'
};

// ========== EMAIL TRANSPORTER ==========
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: { user: CONFIG.email.user, pass: CONFIG.email.pass }
});

// ========== TELEGRAM BOT ==========
const bot = new TelegramBot(CONFIG.telegram.token, { polling: true });

// ========== HELPERS ==========
async function fetchLatestNews() {
  // Would scrape HN, AngelList, Crunchbase for "AI agents" or "intent protocol"
  // For now, return placeholder
  return ['YC S26 batch focused on protocols', 'Meta Muse Spark API private preview open'];
}

async function checkWalletBalance() {
  // Use Solana Web3 or an API to check wallet balance
  // For now, placeholder
  return { sol: 0, usdc: 0 };
}

async function scanInbox() {
  // Use Gmail API to scan for investor-related emails
  // For now, placeholder — real implementation uses googleapis package
  return [];
}

function formatDigest(investorEmails, news, walletBalance) {
  return `📊 *JARVIS DAILY DIGEST*\n
💰 *Wallet:* ${walletBalance.sol} SOL | ${walletBalance.usdc} USDC
📧 *Investor Emails:* ${investorEmails.length} new
  ${investorEmails.map(e => `• ${e.from}: ${e.subject}`).join('\n  ')}
📰 *Top News:*
  ${news.map(n => `• ${n}`).join('\n  ')}
⏰ ${new Date().toLocaleString()}
`;
}

// ========== CORE AGENT LOGIC ==========
async function runDailyDigest() {
  const investorEmails = await scanInbox();
  const news = await fetchLatestNews();
  const wallet = await checkWalletBalance();
  const digest = formatDigest(investorEmails, news, wallet);
  bot.sendMessage(CONFIG.telegram.founderChatId, digest, { parse_mode: 'Markdown' });
}

async function handleInvestorEmail(email) {
  const replyTemplate = `
Hi ${email.from.split(' ')[0]},

Thanks for your interest in INTP (Intent Protocol) — a peer-to-peer fulfillment protocol for AI agents.

Here's what you need:
📄 Litepaper: ${CONFIG.litepaperUrl}
🛠️ GitHub: ${CONFIG.githubUrl}
🎥 Demo Video: ${CONFIG.demoUrl}
💬 Discord: ${CONFIG.discordInvite}
📅 Schedule a call: ${CONFIG.calendlyUrl}

The protocol is live on Ethereum Sepolia with 6 solvers, an open-source Solver SDK, and a 0.1% fee model. Happy to walk you through it.

– Jarvis, Chief of Staff @ INTP Labs
`;
  await transporter.sendMail({
    from: `"Jarvis (INTP Labs)" <${CONFIG.email.user}>`,
    to: email.from,
    subject: `Re: ${email.subject}`,
    text: replyTemplate
  });
}

async function handleLinkedInDraft(postUrl, context) {
  // Generates a draft reply and sends to founder for approval
  const draft = `Sam, you hit the nail on the head — this is system design, not prompt-chaining. We're building the exact fulfillment layer for agentic commerce. Our SolverRegistry is live on Sepolia with 6 solvers. No ask beyond a 15-min stress test. ${CONFIG.calendlyUrl}`;
  bot.sendMessage(CONFIG.telegram.founderChatId, `🔔 *LinkedIn Reply Draft*\nPost: ${postUrl}\n\n${draft}\n\nApprove? /approve_linkedin`, { parse_mode: 'Markdown' });
}

// ========== TELEGRAM COMMANDS ==========
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '🤖 Jarvis online. INTP Labs Chief of Staff ready.\n\n/digest — Run daily report\n/wallet — Check treasury\n/investors — List recent investor emails\n/help — All commands');
});

bot.onText(/\/digest/, (msg) => {
  bot.sendMessage(msg.chat.id, '⏳ Running digest...');
  runDailyDigest().then(() => bot.sendMessage(msg.chat.id, '✅ Digest sent.'));
});

bot.onText(/\/wallet/, async (msg) => {
  const wallet = await checkWalletBalance();
  bot.sendMessage(msg.chat.id, `💰 *INTP Treasury Wallet*\nSOL: ${wallet.sol}\nUSDC: ${wallet.usdc}\nAddress: \`${CONFIG.wallet.address}\``, { parse_mode: 'Markdown' });
});

// ========== SCHEDULED JOBS ==========
// Daily digest at 7:00 AM SAST (5:00 AM UTC)
cron.schedule('0 5 * * *', () => {
  runDailyDigest();
});

// Wallet check every 6 hours
cron.schedule('0 */6 * * *', async () => {
  const wallet = await checkWalletBalance();
  if (wallet.usdc > 10000 || wallet.sol > 100) {
    bot.sendMessage(CONFIG.telegram.founderChatId, `⚠️ *LARGE BALANCE ALERT*\nTreasury has ${wallet.usdc} USDC. Verify manually.`);
  }
});

// ========== STARTUP ==========
console.log('🤖 Jarvis v1.0.0 starting...');
runDailyDigest().then(() => console.log('✅ Initial digest sent.'));
bot.sendMessage(CONFIG.telegram.founderChatId, '🤖 Jarvis is now online. Good morning, Saviours.');
