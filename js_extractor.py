import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import jsbeautifier
from urllib.parse import urljoin
import threading
from concurrent.futures import ThreadPoolExecutor
import re
import os

class JSGrabberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JS Extractor & Security Analyzer")
        self.root.geometry("1100x800")
        self.root.configure(bg="#1e1e1e")
        self.js_files = {}
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#1e1e1e", foreground="#ffffff")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TButton", background="#007acc", foreground="#ffffff", borderwidth=0, focuscolor="none", font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[("active", "#0098ff"), ("disabled", "#555555")])
        style.configure("TEntry", fieldbackground="#2d2d2d", foreground="#ffffff", insertcolor="#ffffff")
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#ffffff", borderwidth=0, padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", "#007acc")], foreground=[("selected", "#ffffff")])

    def create_widgets(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)
        
        label_url = ttk.Label(header_frame, text="Web Sitesi URL:", font=("Helvetica", 10, "bold"))
        label_url.pack(side=tk.LEFT, padx=5)
        
        self.entry_url = ttk.Entry(header_frame, width=50, font=("Helvetica", 10))
        self.entry_url.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entry_url.insert(0, "https://")
        
        self.btn_fetch = ttk.Button(header_frame, text="JS Kodlarını Çek", command=self.start_fetch)
        self.btn_fetch.pack(side=tk.LEFT, padx=5)
        
        self.btn_save = ttk.Button(header_frame, text="Tümünü Kaydet", command=self.save_all_files)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(self.root, padding=10)
        search_frame.pack(fill=tk.X)
        
        label_search = ttk.Label(search_frame, text="Kod İçinde Ara:", font=("Helvetica", 10, "bold"))
        label_search.pack(side=tk.LEFT, padx=5)
        
        self.entry_search = ttk.Entry(search_frame, width=30, font=("Helvetica", 10))
        self.entry_search.pack(side=tk.LEFT, padx=5)
        self.entry_search.bind("<KeyRelease>", self.search_text)
        
        btn_search = ttk.Button(search_frame, text="Ara", command=self.search_text)
        btn_search.pack(side=tk.LEFT, padx=5)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_code = ttk.Frame(notebook)
        self.tab_analysis = ttk.Frame(notebook)
        
        notebook.add(self.tab_code, text="JavaScript Kodları")
        notebook.add(self.tab_analysis, text="Hassas Bilgi Analizi")
        
        self.text_output = scrolledtext.ScrolledText(
            self.tab_code, 
            bg="#1e1e1e", 
            fg="#d4d4d4", 
            insertbackground="#ffffff", 
            font=("Consolas", 10), 
            borderwidth=0
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        self.text_analysis = scrolledtext.ScrolledText(
            self.tab_analysis, 
            bg="#1e1e1e", 
            fg="#ff5555", 
            insertbackground="#ffffff", 
            font=("Consolas", 10), 
            borderwidth=0
        )
        self.text_analysis.pack(fill=tk.BOTH, expand=True)

    def start_fetch(self):
        url = self.entry_url.get().strip()
        if not url:
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, "Lütfen geçerli bir URL girin.\n")
            return
            
        self.btn_fetch.config(state=tk.DISABLED)
        self.text_output.delete(1.0, tk.END)
        self.text_analysis.delete(1.0, tk.END)
        self.text_output.insert(tk.END, "Web sayfası analiz ediliyor...\n")
        
        def worker():
            self.fetch_js_files(url)
            self.root.after(0, self.update_ui)
            
        threading.Thread(target=worker, daemon=True).start()

    def fetch_js_files(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                self.js_files = {f"Erişim başarısız (HTTP {res.status_code})": ""}
                return
                
            soup = BeautifulSoup(res.text, 'html.parser')
            js_urls = []
            for script in soup.find_all('script', src=True):
                js_url = urljoin(url, script['src'])
                js_urls.append(js_url)
                
            self.js_files = {}
            if not js_urls:
                return
                
            def download_file(target_url):
                try:
                    js_res = requests.get(target_url, headers=headers, timeout=10)
                    if js_res.status_code == 200:
                        return target_url, js_res.text, None
                    return target_url, "", f"HTTP {js_res.status_code}"
                except Exception as e:
                    return target_url, "", str(e)
                    
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(download_file, js_urls))
                
            for target_url, content, err in results:
                if err:
                    self.js_files[f"{target_url} ({err})"] = ""
                else:
                    self.js_files[target_url] = content
                    
        except Exception as e:
            self.js_files = {f"Hata: {str(e)}": ""}

    def update_ui(self):
        self.btn_fetch.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_analysis.delete(1.0, tk.END)
        
        if not self.js_files:
            self.text_output.insert(tk.END, "Hiçbir JavaScript dosyası bulunamadı.\n")
            return
            
        all_findings = []
        
        for index, (js_url, content) in enumerate(self.js_files.items(), start=1):
            if content:
                beautified = self.format_js(content)
                self.text_output.insert(tk.END, f"[{index}] {js_url}\n")
                self.text_output.insert(tk.END, "-" * 100 + "\n")
                self.text_output.insert(tk.END, f"{beautified}\n\n" + "=" * 100 + "\n\n")
                
                findings = self.analyze_content(content, js_url)
                if findings:
                    all_findings.extend(findings)
            else:
                self.text_output.insert(tk.END, f"Hata: {js_url}\n\n" + "=" * 100 + "\n\n")
                
        if all_findings:
            for item in all_findings:
                self.text_analysis.insert(tk.END, f"{item}\n")
        else:
            self.text_analysis.insert(tk.END, "Herhangi bir hassas bilgi (API Anahtarı, E-posta, Endpoint vb.) bulunamadı.\n")

    def format_js(self, code):
        try:
            return jsbeautifier.beautify(code)
        except Exception:
            return code

    def analyze_content(self, content, url):
        findings = []
        
        api_pattern = re.compile(r'(?i)(api_key|apikey|secret|token|auth|bearer|password|aws_key|client_secret)\s*[:=]\s*["\']([A-Za-z0-9_\-\.\+\/]{16,})["\']')
        email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        url_pattern = re.compile(r'https?://[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}(?:\/[a-zA-Z0-9_\-\/\.\?\&\=\%]*)?')
        path_pattern = re.compile(r'"(\/[a-zA-Z0-9_\-\/]{2,}(?:\?[a-zA-Z0-9_\-&%=]+)?)"|\'(\/[a-zA-Z0-9_\-\/]{2,}(?:\?[a-zA-Z0-9_\-&%=]+)?)\'')
        
        for m in api_pattern.finditer(content):
            findings.append(f"[{url}] Olası Sır/Anahtar: {m.group(1)} = {m.group(2)}")
            
        for m in email_pattern.finditer(content):
            findings.append(f"[{url}] E-posta Adresi: {m.group(0)}")
            
        for m in url_pattern.finditer(content):
            findings.append(f"[{url}] Harici Bağlantı: {m.group(0)}")
            
        for m in path_pattern.finditer(content):
            val = m.group(1) or m.group(2)
            if val and not val.endswith(('.js', '.png', '.jpg', '.jpeg', '.gif', '.css', '.svg')):
                findings.append(f"[{url}] Dahili Yol/Endpoint: {val}")
                
        return findings

    def search_text(self, event=None):
        self.text_output.tag_remove("match", "1.0", tk.END)
        query = self.entry_search.get()
        if not query:
            return
            
        start_pos = "1.0"
        while True:
            start_pos = self.text_output.search(query, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(query)}c"
            self.text_output.tag_add("match", start_pos, end_pos)
            start_pos = end_pos
            
        self.text_output.tag_config("match", background="#007acc", foreground="#ffffff")

    def save_all_files(self):
        if not self.js_files:
            messagebox.showwarning("Uyarı", "Kaydedilecek dosya bulunamadı. Önce bir siteden JS dosyalarını çekin.")
            return
            
        dest_dir = filedialog.askdirectory()
        if not dest_dir:
            return
            
        saved_count = 0
        for js_url, content in self.js_files.items():
            if content:
                parsed_url = js_url.split('/')[-1].split('?')[0]
                if not parsed_url.endswith('.js'):
                    parsed_url += '.js'
                if not parsed_url or parsed_url == '.js':
                    parsed_url = f"script_{saved_count + 1}.js"
                    
                filepath = os.path.join(dest_dir, parsed_url)
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    saved_count += 1
                except Exception as e:
                    messagebox.showerror("Hata", f"Dosya kaydedilemedi: {parsed_url}\nHata: {e}")
                    
        messagebox.showinfo("Başarılı", f"{saved_count} adet JavaScript dosyası başarıyla kaydedildi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JSGrabberApp(root)
    root.mainloop()
