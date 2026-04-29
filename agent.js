const { Client } = require('@anthropic-ai/sdk');
const nodemailer = require('nodemailer');
const TelegramBot = require('node-telegram-bot-api');
const cron = require('node-cron');
const fs = require('fs');

// ========== CONFIG ==========
const CONFIG = {
  email: {
    user: 'jarvis.intp@gmail.com',
    pass: 'byhw brjp hbxj avlr',
    investorAlias: 'investors@intentprotocol.org'
  },
  telegram: {
    token: '8728930687:AAFm18PEt-mlvZ6rQjiGrPmCAaw5gBG8GG0',
    founderChatId: '6637699767'
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
  return ['YC S26 batch focused on protocols', 'Meta Muse Spark API private preview open'];
}

async function checkWalletBalance() {
  return { sol: 0, usdc: 0 };
}

async function scanInbox() {
  return [];
}

function formatDigest(investorEmails, news, walletBalance) {
  const today = new Date().toLocaleDateString('en-ZA', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  return `📊 *JARVIS DAILY DIGEST — ${today}*\n\n💰 *Treasury:* ${walletBalance.sol} SOL | ${walletBalance.usdc} USDC\n📧 *Investor Inbox:* ${investorEmails.length} new messages\n${investorEmails.map(e => `  • ${e.from}: ${e.subject}`).join('\n')}\n📰 *Market Signals:*\n${news.map(n => `  • ${n}`).join('\n')}\n\n⏰ ${new Date().toLocaleTimeString('en-ZA')} — Jarvis standing by.`;
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
  const replyTemplate = `Hi ${email.from.split(' ')[0]},

Thanks for your interest in INTP (Intent Protocol) — a peer-to-peer fulfillment protocol for AI agents.

Here's what you need:
📄 Litepaper: ${CONFIG.litepaperUrl}
🛠️ GitHub: ${CONFIG.githubUrl}
🎥 Demo Video: ${CONFIG.demoUrl}
💬 Discord: ${CONFIG.discordInvite}
📅 Schedule a call: ${CONFIG.calendlyUrl}

The protocol is live on Ethereum Sepolia with 6 solvers, an open-source Solver SDK, and a 0.1% fee model. Happy to walk you through it.

– Jarvis, Chief of Staff @ INTP Labs`;

  await transporter.sendMail({
    from: `"Jarvis (INTP Labs)" <${CONFIG.email.user}>`,
    to: email.from,
    subject: `Re: ${email.subject}`,
    text: replyTemplate
  });
}

// ========== TELEGRAM COMMANDS ==========
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '🤖 Jarvis online. INTP Labs Chief of Staff ready.\n\n/digest — Run daily report\n/wallet — Check treasury\n/investors — List recent investor emails\n/help — All commands');
});

bot.onText(/\/digest/, async (msg) => {
  bot.sendMessage(msg.chat.id, '⏳ Running digest...');
  await runDailyDigest();
});

bot.onText(/\/wallet/, async (msg) => {
  const wallet = await checkWalletBalance();
  bot.sendMessage(msg.chat.id, `💰 *INTP Treasury Wallet*\nSOL: ${wallet.sol}\nUSDC: ${wallet.usdc}\nAddress: \`${CONFIG.wallet.address}\``, { parse_mode: 'Markdown' });
});

bot.onText(/\/help/, (msg) => {
  bot.sendMessage(msg.chat.id, '🤖 *Jarvis Commands*\n/digest — Daily report\n/wallet — Treasury balance\n/investors — Investor emails\n/help — All commands', { parse_mode: 'Markdown' });
});

// ========== SCHEDULED JOBS ==========
cron.schedule('0 5 * * *', () => {
  runDailyDigest();
});

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
