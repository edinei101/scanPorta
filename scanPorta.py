import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

# ======================================
# scanPorta
# Ferramenta para varredura de portas TCP/UDP
# Autor: Edinei
# ======================================

def escanear_tcp(ip, porta, caixa_texto):
    """Faz a varredura TCP (tentativa de conexão)."""
    try:
        soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soquete.settimeout(1)
        resultado = soquete.connect_ex((ip, porta))
        soquete.close()
        if resultado == 0:
            atualizar_texto(caixa_texto, f"[TCP] Porta {porta} ABERTA\n")
        else:
            atualizar_texto(caixa_texto, f"[TCP] Porta {porta} FECHADA\n")
    except Exception:
        atualizar_texto(caixa_texto, f"[TCP] Porta {porta} FILTRADA\n")

def escanear_udp(ip, porta, caixa_texto):
    """Faz a varredura UDP enviando pacote vazio."""
    try:
        soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soquete.settimeout(1)
        soquete.sendto(b"", (ip, porta))
        try:
            soquete.recvfrom(1024)
            atualizar_texto(caixa_texto, f"[UDP] Porta {porta} ABERTA (respondeu)\n")
        except socket.timeout:
            atualizar_texto(caixa_texto, f"[UDP] Porta {porta} POSSIVELMENTE ABERTA/FILTRADA\n")
    except Exception:
        atualizar_texto(caixa_texto, f"[UDP] Porta {porta} FILTRADA\n")
    finally:
        soquete.close()

def atualizar_texto(caixa_texto, mensagem):
    """Atualiza a área de texto na interface."""
    caixa_texto.insert(tk.END, mensagem)
    caixa_texto.see(tk.END)

def iniciar_varredura(ip, porta_inicial, porta_final, usar_udp, caixa_texto):
    """Inicia a varredura em uma faixa de portas."""
    atualizar_texto(caixa_texto, f"\nIniciando varredura em {ip} (Portas {porta_inicial}-{porta_final})\n")
    atualizar_texto(caixa_texto, "-" * 50 + "\n")
    for porta in range(porta_inicial, porta_final + 1):
        t_tcp = threading.Thread(target=escanear_tcp, args=(ip, porta, caixa_texto))
        t_tcp.start()
        if usar_udp:
            t_udp = threading.Thread(target=escanear_udp, args=(ip, porta, caixa_texto))
            t_udp.start()

def main():
    janela = tk.Tk()
    janela.title("scanPorta")
    janela.geometry("650x420")
    janela.configure(bg="#1E3A5F")  # Azul escuro

    # Caminho do ícone (funciona no Python ou exe do PyInstaller)
    caminho_base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    caminho_icone = os.path.join(caminho_base, "icone.ico")
    janela.iconbitmap(caminho_icone)

    fonte_padrao = ("Arial", 10)
    estilo = ttk.Style()
    estilo.theme_use("clam")

    # Estilo dos widgets
    estilo.configure("TLabel", background="#1E3A5F", foreground="white", font=fonte_padrao)
    estilo.configure("TButton", background="#2E5C9A", foreground="white", font=fonte_padrao, padding=6)
    estilo.map("TButton", background=[("active", "#3E7BC1")], foreground=[("active", "white")])
    estilo.configure("TCheckbutton", background="#1E3A5F", foreground="white", font=fonte_padrao)

    # Frame para entradas
    frame = ttk.Frame(janela, padding=10)
    frame.pack(fill="x")

    ttk.Label(frame, text="IP Alvo:").grid(column=0, row=0, sticky="w")
    entrada_ip = ttk.Entry(frame, width=20, font=fonte_padrao)
    entrada_ip.grid(column=1, row=0, padx=5)

    ttk.Label(frame, text="Porta Inicial:").grid(column=2, row=0, sticky="w")
    entrada_porta_inicial = ttk.Entry(frame, width=6, font=fonte_padrao)
    entrada_porta_inicial.grid(column=3, row=0, padx=5)

    ttk.Label(frame, text="Porta Final:").grid(column=4, row=0, sticky="w")
    entrada_porta_final = ttk.Entry(frame, width=6, font=fonte_padrao)
    entrada_porta_final.grid(column=5, row=0, padx=5)

    usar_udp = tk.BooleanVar()
    chk_udp = ttk.Checkbutton(frame, text="Ativar UDP", variable=usar_udp)
    chk_udp.grid(column=6, row=0, padx=5)

    # Área de resultados
    caixa_texto = scrolledtext.ScrolledText(janela, wrap=tk.WORD, height=15, font=("Arial", 10))
    caixa_texto.pack(fill="both", expand=True, padx=10, pady=10)
    caixa_texto.configure(bg="#E6EEF8", fg="black")  # Azul claro

    # Botão iniciar
    def ao_clicar_iniciar():
        ip = entrada_ip.get()
        try:
            porta_inicial = int(entrada_porta_inicial.get())
            porta_final = int(entrada_porta_final.get())
        except ValueError:
            atualizar_texto(caixa_texto, "⚠️ Digite portas válidas!\n")
            return
        threading.Thread(target=iniciar_varredura,
                         args=(ip, porta_inicial, porta_final, usar_udp.get(), caixa_texto)).start()

    botao_iniciar = ttk.Button(janela, text="Iniciar Varredura", command=ao_clicar_iniciar)
    botao_iniciar.pack(pady=5)

    janela.mainloop()

if __name__ == "__main__":
    main()
