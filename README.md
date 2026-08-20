# EchoBot — VPS Hosting & Deployment Guide

This README documents how to host, run, update, monitor, and troubleshoot EchoBot on an Ubuntu VPS using Python, a virtual environment, and `systemd`.

## Current Deployment

| Item | Value |
|---|---|
| VPS provider | InterServer |
| OS | Ubuntu 24.04 LTS |
| Project directory | `/root/BotFolder` |
| Main bot file | `/root/BotFolder/EchoBot.py` |
| Virtual environment | `/root/BotFolder/venv` |
| systemd service | `echobot` |
| Service file | `/etc/systemd/system/echobot.service` |

The bot is managed by `systemd`, so it continues running after you close SSH and automatically starts after a VPS reboot.

---

## 1. Connect to the VPS

```bash
ssh root@YOUR_VPS_IP
```

Example:

```bash
ssh root@162.35.183.234
```

If SSH reports `REMOTE HOST IDENTIFICATION HAS CHANGED` and you intentionally reinstalled/rebuilt the VPS:

```bash
ssh-keygen -f "/home/daniel/.ssh/known_hosts" -R "YOUR_VPS_IP"
```

Then connect again:

```bash
ssh root@YOUR_VPS_IP
```

Only remove the old key when you know the server was legitimately reinstalled or its SSH host key changed.

Leave SSH with:

```bash
exit
```

Closing SSH does **not** stop EchoBot when it is managed by `systemd`.

---

## 2. Initial VPS Setup

```bash
apt update
apt upgrade -y
apt install python3 python3-pip python3-venv -y
```

Check Python:

```bash
python3 --version
```

---

## 3. Project Structure

Expected structure:

```text
/root/BotFolder/
├── EchoBot.py
├── requirements.txt
├── venv/
└── other project files...
```

Go to the project:

```bash
cd /root/BotFolder
```

Check files:

```bash
ls -lah
pwd
```

---

## 4. Python Virtual Environment

Create:

```bash
cd /root/BotFolder
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Leave the environment:

```bash
deactivate
```

---

## 5. Install Dependencies

If `requirements.txt` exists:

```bash
cd /root/BotFolder
source venv/bin/activate
pip install -r requirements.txt
```

For the Telegram library, if needed:

```bash
pip install python-telegram-bot
```

Save installed dependencies:

```bash
pip freeze > requirements.txt
```

---

## 6. Test the Bot Manually

```bash
cd /root/BotFolder
source venv/bin/activate
python EchoBot.py
```

Stop a manually running bot with:

```text
Ctrl + C
```

### Important

Once `systemd` manages EchoBot, do **not** run:

```bash
python EchoBot.py
```

while the systemd service is already running. Two polling instances can cause:

```text
telegram.error.Conflict:
Conflict: terminated by other getUpdates request;
make sure that only one bot instance is running
```

---

## 7. systemd Service

Service file:

```text
/etc/systemd/system/echobot.service
```

Configuration:

```ini
[Unit]
Description=EchoBot Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/BotFolder
ExecStart=/root/BotFolder/venv/bin/python /root/BotFolder/EchoBot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Create/edit:

```bash
nano /etc/systemd/system/echobot.service
```

After changing the service file:

```bash
systemctl daemon-reload
```

Enable at boot:

```bash
systemctl enable echobot
```

Start:

```bash
systemctl start echobot
```

---

## 8. Check Bot Status

```bash
systemctl status echobot
```

Healthy status:

```text
Active: active (running)
```

The process should point to:

```text
/root/BotFolder/venv/bin/python /root/BotFolder/EchoBot.py
```

---

## 9. Start, Stop, and Restart

Start:

```bash
systemctl start echobot
```

Stop:

```bash
systemctl stop echobot
```

Restart:

```bash
systemctl restart echobot
```

Check:

```bash
systemctl status echobot
```

---

## 10. View Logs

Live logs:

```bash
journalctl -u echobot -f
```

Press `Ctrl + C` to leave the log viewer. This does **not** stop the bot.

Recent 100 lines:

```bash
journalctl -u echobot -n 100 --no-pager
```

Recent 200 lines:

```bash
journalctl -u echobot -n 200 --no-pager
```

Today's logs:

```bash
journalctl -u echobot --since today
```

Last hour:

```bash
journalctl -u echobot --since "1 hour ago"
```

---

## 11. Check Running EchoBot Processes

```bash
pgrep -af EchoBot
```

Or:

```bash
ps aux | grep EchoBot
```

Normally there should be only **one actual EchoBot process** when using Telegram polling.

---

## 12. Avoid Telegram Conflict Errors

If you see:

```text
telegram.error.Conflict:
Conflict: terminated by other getUpdates request;
make sure that only one bot instance is running
```

another copy of EchoBot is using the same Telegram bot token.

Possible causes:

- EchoBot was started manually in a terminal.
- `systemd` is already running EchoBot.
- The old PythonAnywhere bot is still running.
- Another VPS is running the same bot.
- Another computer is running the same bot.

Check this VPS:

```bash
pgrep -af EchoBot
```

Identify unwanted processes:

```bash
ps aux | grep EchoBot
```

Stop an unwanted process by PID:

```bash
kill PID
```

Example:

```bash
kill 3952
```

Then:

```bash
systemctl restart echobot
```

If the bot was migrated from PythonAnywhere, make sure the old PythonAnywhere instance is stopped.

Only one polling instance should use the bot token.

---

## 13. Updating the Bot with Git

### On your local computer

```bash
git status
git add .
git commit -m "Update bot"
git push
```

### On the VPS

```bash
ssh root@YOUR_VPS_IP
cd /root/BotFolder
git pull
systemctl restart echobot
```

Then:

```bash
systemctl status echobot
```

Monitor:

```bash
journalctl -u echobot -f
```

### Normal update workflow

For ordinary code changes:

```bash
cd /root/BotFolder
git pull
systemctl restart echobot
```

That is normally all you need.

---

## 14. If `requirements.txt` Changed

```bash
cd /root/BotFolder
git pull
source venv/bin/activate
pip install -r requirements.txt
systemctl restart echobot
```

Then:

```bash
systemctl status echobot
```

---

## 15. If the systemd Service File Changed

After changing `/etc/systemd/system/echobot.service`:

```bash
systemctl daemon-reload
systemctl restart echobot
```

For a normal `EchoBot.py` change, `daemon-reload` is **not** required.

---

## 16. Git Repository Commands

Check remote:

```bash
cd /root/BotFolder
git remote -v
```

Check branch:

```bash
git branch
```

Check status:

```bash
git status
```

Pull:

```bash
git pull
```

---

## 17. Editing the Bot on the VPS

```bash
cd /root/BotFolder
nano EchoBot.py
```

After editing:

```bash
systemctl restart echobot
```

Then:

```bash
journalctl -u echobot -f
```

If using Git, it is generally better to edit locally, commit, push, and pull on the VPS.

---

## 18. Automatic Restart

The service uses:

```ini
Restart=always
RestartSec=5
```

If the bot crashes, systemd will attempt to restart it.

If it repeatedly restarts, inspect the actual error:

```bash
journalctl -u echobot -n 100 --no-pager
```

---

## 19. VPS Reboot

```bash
reboot
```

Because the service is enabled:

```bash
systemctl enable echobot
```

EchoBot should automatically start after Ubuntu boots.

After reconnecting:

```bash
systemctl status echobot
```

---

## 20. Enable or Disable Automatic Startup

Enable:

```bash
systemctl enable echobot
```

Disable:

```bash
systemctl disable echobot
```

Check:

```bash
systemctl is-enabled echobot
```

Expected:

```text
enabled
```

---

## 21. Troubleshooting

### `status=203/EXEC`

Check the service:

```bash
cat /etc/systemd/system/echobot.service
```

Check Python:

```bash
ls -lah /root/BotFolder/venv/bin/python
```

Check bot:

```bash
ls -lah /root/BotFolder/EchoBot.py
```

The service should contain:

```ini
WorkingDirectory=/root/BotFolder
ExecStart=/root/BotFolder/venv/bin/python /root/BotFolder/EchoBot.py
```

Then:

```bash
systemctl daemon-reload
systemctl restart echobot
```

### `ModuleNotFoundError`

Activate the environment:

```bash
cd /root/BotFolder
source venv/bin/activate
pip install -r requirements.txt
```

If Telegram is missing:

```bash
pip install python-telegram-bot
```

Restart:

```bash
systemctl restart echobot
```

### Telegram `Conflict`

```bash
pgrep -af EchoBot
```

Stop duplicate instances and make sure PythonAnywhere/other servers are not running the same bot.

Then:

```bash
systemctl restart echobot
```

### Bot is running but does not respond

Check:

```bash
systemctl status echobot
journalctl -u echobot -f
pgrep -af EchoBot
```

If the bot uses external APIs, inspect the logs for API errors, timeouts, HTTP errors, database errors, or invalid responses.

---

## 22. Debugging Commands That Sometimes Fail

If a command such as `/withdraw` works for some users but intermittently fails, start live logging:

```bash
journalctl -u echobot -f
```

Reproduce the problem and inspect for:

- `Traceback`
- `Exception`
- `Timeout`
- `telegram.error`
- `requests.exceptions`
- `HTTPError`
- database errors
- JSON errors
- API response errors

For payment/API commands, also check:

- HTTP status codes
- API response body
- request timeout
- database transactions
- duplicate requests
- concurrent requests
- user/account balance
- exception handling

Avoid silently swallowing exceptions.

---

## 23. Security

Never commit or expose:

- Telegram bot token
- API keys
- Payment secret keys
- Database passwords
- Firebase service-account credentials
- SSH private keys
- JWT secrets
- Encryption keys

Do not put secrets into GitHub.

Use environment variables or secure secret management.

If a secret is accidentally committed, rotate/revoke it immediately. Removing it from the latest file does not remove it from Git history.

---

## 24. Quick Reference

### Go to bot

```bash
cd /root/BotFolder
```

### Activate environment

```bash
source /root/BotFolder/venv/bin/activate
```

### Check status

```bash
systemctl status echobot
```

### Start

```bash
systemctl start echobot
```

### Stop

```bash
systemctl stop echobot
```

### Restart

```bash
systemctl restart echobot
```

### Live logs

```bash
journalctl -u echobot -f
```

### Recent logs

```bash
journalctl -u echobot -n 100 --no-pager
```

### Check processes

```bash
pgrep -af EchoBot
```

### Git status

```bash
git status
```

### Pull latest code

```bash
git pull
```

### Install dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Reload systemd

```bash
systemctl daemon-reload
```

### Enable on boot

```bash
systemctl enable echobot
```

### Disable on boot

```bash
systemctl disable echobot
```

---

## 25. Recommended Deployment Workflow

### Local computer

```bash
git add .
git commit -m "Describe changes"
git push
```

### VPS

```bash
cd /root/BotFolder
git pull
systemctl restart echobot
systemctl status echobot
```

Live logs:

```bash
journalctl -u echobot -f
```

If dependencies changed:

```bash
source venv/bin/activate
pip install -r requirements.txt
systemctl restart echobot
```

---

## 26. Architecture

```text
                    Telegram
                       |
                       v
                Telegram Bot API
                       |
                       v
              +------------------+
              | InterServer VPS  |
              | Ubuntu 24.04     |
              +--------+---------+
                       |
                       v
               /root/BotFolder
                       |
                       v
                  Python venv
                       |
                       v
                  EchoBot.py
                       |
                       v
                systemd: echobot
                  /                            /                             v               v
        Auto-start on      Auto-restart
          VPS reboot       after failure
```

---

## 27. Final Daily Cheat Sheet

For a normal code update:

```bash
cd /root/BotFolder
git pull
systemctl restart echobot
systemctl status echobot
```

For live debugging:

```bash
journalctl -u echobot -f
```

For checking duplicate instances:

```bash
pgrep -af EchoBot
```

For dependency updates:

```bash
cd /root/BotFolder
git pull
source venv/bin/activate
pip install -r requirements.txt
systemctl restart echobot
```

For systemd configuration changes:

```bash
systemctl daemon-reload
systemctl restart echobot
```

---

## Important Rule

**Do not run a second copy of EchoBot manually while the systemd service is active.**

Use:

```bash
systemctl restart echobot
```

instead of:

```bash
python EchoBot.py
```

This prevents Telegram polling conflicts and keeps the VPS deployment under one process manager.
