## 🕶️ Shodan Black Hat — 2025 Edition

**Shodan Black Hat** is an advanced command-line tool that leverages the power of the [Shodan.io](https://shodan.io) search engine to find exposed devices and services on the internet — wrapped in a modern interface with rich output, dark-mode terminal UI, and flexible query modes.

> ⚠️ For educational and research purposes only. Unauthorized scanning or usage against networks you do not own is **illegal**.

---

### 🧐 Features

* 🔍 Keyword-based Shodan search (`--query`)
* 🔗 Website scanning via `--url` (auto-resolves to IP)
* 🌐 Direct IP lookup with `--ip`
* 📄 Export results to:

  * JSON (`sendata.json`)
  * CSV (`sendata.csv`)
* 🎨 Rich terminal UI with dark mode (via `rich`)
* 📊 Result display in elegant table format
* 💾 Shodan API key stored securely in `apikey.json` (prompted once)
* 🚀 Fast & lightweight — perfect for recon workflows and threat research

---

### 💪 Installation

```bash
git clone https://github.com/devkumarswipe/shodan-black-hat.git
cd shodan-black-hat
pip install -r requirements.txt
```

> **Requirements:**
>
> * Python 3.8+
> * [Shodan Python Library](https://pypi.org/project/shodan/)
> * `rich`

---

### 🔐 Getting Started

Before first use, obtain your [Shodan API Key](https://account.shodan.io) and keep it ready.

Run the tool:

```bash
python3 blacked.py
```

It will prompt:

```
[+] Enter your Shodan API Key:
```

Your key is saved to `apikey.json` and reused securely.

---

### ⚙️ Usage Examples

#### 🔎 Search by Shodan query:

```bash
python3 blacked.py --query "apache" --limit 10
```

#### 🌐 Scan a website (auto IP resolve):

```bash
python3 blacked.py --url https://example.com
```

#### 🧽 Lookup direct IP:

```bash
python3 blacked.py --ip 1.2.3.4
```

#### 📄 Export to CSV:

```bash
python3 blacked.py --query nginx --csv
```

---

### 📁 Output Files

| File Name      | Description                    |
| -------------- | ------------------------------ |
| `apikey.json`  | Stores your Shodan API key     |
| `sendata.json` | Full result dump (JSON format) |
| `sendata.csv`  | Cleaned result export (CSV)    |

---

### 🧑‍💻 Developed By

**Ved Kumar**
---

### ⚠️ Legal Disclaimer

This tool is provided **for educational use only**. Use it responsibly.

You are solely responsible for your actions. Accessing or scanning systems without permission is **illegal** and punishable under law.
