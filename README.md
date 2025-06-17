# WebPayloadForge 🔥

```
██╗    ██╗███████╗██████╗     ██████╗  █████╗ ██╗  ██╗██╗      ██████╗ ███████╗██████╗ ███████╗
██║    ██║██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██║  ██║██║     ██╔═══██╗██╔════╝██╔══██╗██╔════╝
██║ █╗ ██║█████╗  ██████╔╝    ██████╔╝███████║███████║██║     ██║   ██║█████╗  ██████╔╝█████╗  
██║███╗██║██╔══╝  ██╔══██╗    ██╔═══╝ ██╔══██║██╔══██║██║     ██║   ██║██╔══╝  ██╔══██╗██╔══╝  
╚███╔███╔╝███████╗██████╔╝    ██║     ██║  ██║██║  ██║███████╗╚██████╔╝██║     ██║  ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝
```

A powerful and modular payload generation tool for web security testing and exploitation.

## 🌟 Features

### Core Functionality
- **XSS Payload Generator**
  - Reflected, stored, and DOM-based payloads
  - Advanced bypass techniques
  - SVG and event handler variations
  - WAF evasion techniques

- **SQL Injection Payload Generator**
  - Error-based, union-based, and blind SQLi
  - WAF evasion techniques
  - Special character variations
  - Database-specific payloads

- **Command Injection Payload Generator**
  - Linux and Windows payload variants
  - Multiple execution methods
  - Environment-specific payloads

### Advanced Features
- **Multiple Encoding Options**
  - Base64
  - URL encoding
  - Hex encoding
  - Unicode encoding
  - HTML encoding
  - Binary encoding
  - Octal encoding

- **Obfuscation Techniques**
  - Comment insertion
  - Character spacing
  - Mixed case
  - Combined techniques

- **Output Formats**
  - Command-line interface
  - JSON export
  - Clipboard copy
  - GUI interface

### Integration
- Burp Suite integration
- WAF bypass test cases
- Real-world filter bypasses

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/WebPayloadForge.git

# Navigate to the project directory
cd WebPayloadForge

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Command Line Interface
```bash
# Generate XSS payloads
python webpayloadforge.py --xss --type reflected

# Generate SQL injection payloads
python webpayloadforge.py --sqli --type union

# Generate command injection payloads
python webpayloadforge.py --cmd --os windows

# Encode payloads
python webpayloadforge.py --xss --encode base64

# Export to JSON
python webpayloadforge.py --xss --output json --file payloads.json

# Copy to clipboard
python webpayloadforge.py --sqli --output clipboard
```

### GUI Interface
```bash
# Launch the GUI
python webpayloadforge_gui.py
```

## 📁 Project Structure
```
WebPayloadForge/
├── webpayloadforge.py          # Main CLI script
├── webpayloadforge_gui.py      # GUI interface
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── sample_payloads.json        # Example payloads
└── waf_bypass_rules.json       # WAF bypass test cases
```

## 🔧 Configuration

### WAF Bypass Rules
The `waf_bypass_rules.json` file contains predefined WAF bypass techniques for:
- XSS attacks
- SQL injection
- Command injection

### Custom Payloads
You can add custom payloads by modifying the respective sections in the main script.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Always obtain proper authorization before testing any system. The authors are not responsible for any misuse or damage caused by this program.

## 🙏 Acknowledgments

- Inspired by various security testing tools
- Thanks to the open-source community
- Special thanks to all contributors 