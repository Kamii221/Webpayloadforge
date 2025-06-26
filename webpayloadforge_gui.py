import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from webpayloadforge import PayloadGenerator
import pyperclip
import threading
import requests
from urllib.parse import urlparse

# Create res/payloads directory if it doesn't exist
os.makedirs('res/payloads', exist_ok=True)

class WebPayloadForgeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WebPayloadForge")
        self.root.geometry("800x600")
        self.generator = PayloadGenerator()
        self.payloads_dir = 'res/payloads'
        self.setup_gui()

    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Payload Type Selection
        ttk.Label(main_frame, text="Payload Type:").grid(row=0, column=0, sticky=tk.W)
        self.payload_type = ttk.Combobox(main_frame, values=["XSS", "SQL Injection", "Command Injection"])
        self.payload_type.grid(row=0, column=1, sticky=tk.W)
        self.payload_type.bind('<<ComboboxSelected>>', self.update_subtype)

        # Subtype Selection
        ttk.Label(main_frame, text="Subtype:").grid(row=1, column=0, sticky=tk.W)
        self.subtype = ttk.Combobox(main_frame)
        self.subtype.grid(row=1, column=1, sticky=tk.W)

        # OS Selection (for Command Injection)
        ttk.Label(main_frame, text="OS:").grid(row=2, column=0, sticky=tk.W)
        self.os_type = ttk.Combobox(main_frame, values=["Windows", "Linux"])
        self.os_type.grid(row=2, column=1, sticky=tk.W)

        # Encoding Options
        ttk.Label(main_frame, text="Encoding:").grid(row=3, column=0, sticky=tk.W)
        self.encoding = ttk.Combobox(main_frame, values=["None", "Base64", "URL", "Hex", "Unicode", "HTML", "Binary", "Octal"])
        self.encoding.grid(row=3, column=1, sticky=tk.W)

        # Obfuscation Options
        ttk.Label(main_frame, text="Obfuscation:").grid(row=4, column=0, sticky=tk.W)
        self.obfuscation = ttk.Combobox(main_frame, values=["None", "Comments", "Spacing", "Mixed Case", "All"])
        self.obfuscation.grid(row=4, column=1, sticky=tk.W)

        # Output Options
        ttk.Label(main_frame, text="Output:").grid(row=5, column=0, sticky=tk.W)
        self.output_frame = ttk.Frame(main_frame)
        self.output_frame.grid(row=5, column=1, sticky=tk.W)
        
        self.clipboard_var = tk.BooleanVar()
        ttk.Checkbutton(self.output_frame, text="Clipboard", variable=self.clipboard_var).pack(side=tk.LEFT)
        
        self.json_var = tk.BooleanVar()
        ttk.Checkbutton(self.output_frame, text="JSON", variable=self.json_var).pack(side=tk.LEFT)

        # ZAP Proxy Integration
        ttk.Label(main_frame, text="ZAP Target URL:").grid(row=6, column=0, sticky=tk.W)
        self.zap_target_url = ttk.Entry(main_frame, width=40)
        self.zap_target_url.grid(row=6, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="ZAP API URL:").grid(row=7, column=0, sticky=tk.W)
        self.zap_api_url = ttk.Entry(main_frame, width=40)
        self.zap_api_url.grid(row=7, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="ZAP API Key:").grid(row=8, column=0, sticky=tk.W)
        self.zap_api_key = ttk.Entry(main_frame, width=40, show='*')
        self.zap_api_key.grid(row=8, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="HTTP Method:").grid(row=9, column=0, sticky=tk.W)
        self.http_method = ttk.Combobox(main_frame, values=["GET", "POST"])
        self.http_method.set("GET")
        self.http_method.grid(row=9, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="Parameter:").grid(row=10, column=0, sticky=tk.W)
        self.param = ttk.Entry(main_frame, width=20)
        self.param.insert(0, "id")
        self.param.grid(row=10, column=1, sticky=tk.W)

        # Generate Button
        ttk.Button(main_frame, text="Generate Payloads", command=self.generate_payloads).grid(row=11, column=0, columnspan=2, pady=10)

        # Output Area
        self.output_area = scrolledtext.ScrolledText(main_frame, width=80, height=20)
        self.output_area.grid(row=12, column=0, columnspan=2, pady=10)

    def update_subtype(self, event=None):
        payload_type = self.payload_type.get()
        if payload_type == "XSS":
            self.subtype['values'] = ["Reflected", "Stored", "DOM"]
        elif payload_type == "SQL Injection":
            self.subtype['values'] = ["Error", "Union", "Blind"]
        elif payload_type == "Command Injection":
            self.subtype['values'] = ["Basic", "Advanced"]

    def obfuscate_payload(self, payload, obfuscation_type):
        if obfuscation_type == "None":
            return payload
        elif obfuscation_type == "Comments":
            return f"/*{payload}*/"
        elif obfuscation_type == "Spacing":
            return " ".join(payload)
        elif obfuscation_type == "Mixed Case":
            return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(payload))
        elif obfuscation_type == "All":
            payload = self.obfuscate_payload(payload, "Comments")
            payload = self.obfuscate_payload(payload, "Spacing")
            return self.obfuscate_payload(payload, "Mixed Case")
        return payload

    def send_to_zap(self, payloads):
        target_url = self.zap_target_url.get()
        api_url = self.zap_api_url.get()
        api_key = self.zap_api_key.get()
        method = self.http_method.get()
        param = self.param.get()
        if not (target_url and api_url and api_key):
            messagebox.showerror("Error", "ZAP Target URL, API URL, and API Key are required.")
            return
        try:
            self.generator.send_to_zap(payloads, target_url, api_url, api_key, method, param)
            messagebox.showinfo("Success", "Payloads sent to ZAP proxy.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send to ZAP: {str(e)}")

    def generate_payloads(self):
        try:
            payload_type = self.payload_type.get().lower()
            subtype = self.subtype.get().lower()
            encoding = self.encoding.get().lower()
            obfuscation = self.obfuscation.get()
            os_type = self.os_type.get().lower() if self.os_type.get() else None

            # Generate payloads
            if payload_type == "xss":
                payloads = self.generator.generate_xss(subtype, encoding)
            elif payload_type == "sql injection":
                payloads = self.generator.generate_sqli(subtype, encoding)
            elif payload_type == "command injection":
                payloads = self.generator.generate_cmd(os_type, encoding)

            # Apply obfuscation
            if obfuscation != "None":
                payloads = [self.obfuscate_payload(p, obfuscation) for p in payloads]

            # Display payloads
            self.output_area.delete(1.0, tk.END)
            for payload in payloads:
                self.output_area.insert(tk.END, f"{payload}\n")

            # Always copy to clipboard
            pyperclip.copy('\n'.join(payloads))
            messagebox.showinfo("Success", "Payloads copied to clipboard")

            if self.json_var.get():
                filename = os.path.join(self.payloads_dir, 'payloads.json')
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(payloads, f, indent=4)
                messagebox.showinfo("Success", f"Payloads saved to {filename}")

            # Send to ZAP proxy if all required fields are filled
            if self.zap_target_url.get() and self.zap_api_url.get() and self.zap_api_key.get():
                self.send_to_zap(payloads)

        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = WebPayloadForgeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
