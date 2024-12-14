import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

# Nome do arquivo JSON
DATABASE_FILE = "clinica_data.json"

def load_data():
    """Carrega os dados do arquivo JSON."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Retorna lista vazia se o JSON estiver corrompido
    else:
        return []

def save_data(data):
    """Salva os dados no arquivo JSON."""
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def search_patient():
    """Função para buscar pacientes."""
    search_term = search_entry.get().lower()
    results = [p for p in pacientes if search_term in p['nome'].lower()]
    update_treeview(results)

def edit_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showinfo("Aviso", "Selecione um paciente para editar.")
        return

    # Obtém o índice armazenado diretamente nos valores do item da Treeview
    index = tree.item(selected_item[0])['values'][0] - 1

    patient = pacientes[index]

    # ... (campos de entrada para nome, telefone e email)
    
    edit_window = tk.Tk()  # Create the edit window here
    edit_window.title("Editar Paciente")
    edit_window.configure(bg="#A801A2")

    nome_label = tk.Label(edit_window, text="Nome:", font=("Arial",12), bg="#A801A2", fg="#ffffff")
    nome_label.grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(edit_window, font=("Arial",12))
    nome_entry.insert(0, patient['nome'])
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    telefone_label = tk.Label(edit_window, text="Telefone:", font=("Arial",12), bg="#A801A2", fg="#ffffff")
    telefone_label.grid(row=1, column=0, padx=5, pady=5)
    telefone_entry = tk.Entry(edit_window, font=("Arial",12))
    telefone_entry.insert(0, patient['telefone'])
    telefone_entry.grid(row=1, column=1, padx=5, pady=5)

    email_label = tk.Label(edit_window, text="Email:", font=("Arial",12), bg="#A801A2", fg="#ffffff")
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(edit_window, font=("Arial",12))
    email_entry.insert(0, patient['email'])
    email_entry.grid(row=2, column=1, padx=5, pady=5)


    def ver_prontuario():
        prontuario_window = tk.Toplevel(edit_window)  # Janela filha da janela de edição
        prontuario_window.title("Prontuário de " + patient['nome'])
        prontuario_window.configure(bg="#4F004A")

        def salvar_prontuario():
          patient['prontuario'] = prontuario_texto.get("1.0", tk.END)
          save_data(pacientes)
          prontuario_window.destroy()

        # Widgets para o prontuário
        prontuario_texto = scrolledtext.ScrolledText(prontuario_window, wrap=tk.WORD) # Widget de texto com scrollbar
        if 'prontuario' in patient: #verifica se ja existe o prontuario.
          prontuario_texto.insert(tk.END, patient['prontuario'])
        prontuario_texto.pack(fill="both", expand=True, padx=10, pady=10)

        botao_salvar_prontuario = tk.Button(prontuario_window, text="Salvar Prontuário", command=salvar_prontuario, font=("Arial",12,"bold"), bg="#00FFCC", fg="#5F0026")
        botao_salvar_prontuario.pack(pady=10)

        prontuario_window.protocol("WM_DELETE_WINDOW", salvar_prontuario) #chamado quando fecha a janela

    prontuario_button = tk.Button(edit_window, text="Ver Prontuário", command=ver_prontuario, font=("Arial",12,"bold"), bg="#01E778", fg="#537103")
    prontuario_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def save_edit():
        patient['nome'] = nome_entry.get()
        patient['telefone'] = telefone_entry.get()
        patient['email'] = email_entry.get()
        save_data(pacientes)
        update_treeview(pacientes)
        edit_window.destroy()
        
    save_button = tk.Button(edit_window, text="Salvar Edições", command=save_edit, font=("Arial",12,"bold"), bg="#F1E903", fg="#0029AD")
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

def delete_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showinfo("Aviso", "Selecione um paciente para deletar.")
        return

    if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este paciente?"):
        index = tree.item(selected_item[0])['values'][0]-1
        del pacientes[index]
        save_data(pacientes)
        update_treeview(pacientes)

def add_patient():
    """Função para adicionar um novo paciente."""
    add_window = tk.Toplevel(root)
    add_window.title("Adicionar Paciente")
    add_window.configure(bg="#03D7DF")

    nome_label = tk.Label(add_window, text="Nome:", font=("Arial",12), bg="#03D7DF")
    nome_label.grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(add_window, font=("Arial",12))
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    telefone_label = tk.Label(add_window, text="Telefone:", font=("Arial",12), bg="#03D7DF")
    telefone_label.grid(row=1, column=0, padx=5, pady=5)
    telefone_entry = tk.Entry(add_window, font=("Arial",12))
    telefone_entry.grid(row=1, column=1, padx=5, pady=5)

    # Outros campos:
    email_label = tk.Label(add_window, text="Email:", font=("Arial",12), bg="#03D7DF")
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(add_window, font=("Arial",12))
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    def save_new_patient():
        nome = nome_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()

        if not nome or not telefone:  # Validação básica
            messagebox.showerror("Erro", "Nome e Telefone são obrigatórios.")
            return

        novo_paciente = {
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "prontuario": ""
        }
        pacientes.append(novo_paciente)
        save_data(pacientes)
        update_treeview(pacientes)
        add_window.destroy()

    save_button = tk.Button(add_window, text="Salvar", command=save_new_patient, font=("Arial",12,"bold"), bg="#6D6402", fg="#ffffff")
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

def update_treeview(data):
    tree.delete(*tree.get_children())
    for i, paciente in enumerate(data):
        tree.insert("", tk.END, values=(i + 1, paciente['nome'], paciente.get('telefone', 'N/A'), paciente.get('email', 'N/A')))

# Carrega os dados
pacientes = load_data()

# Interface gráfica
root = tk.Tk()
root.title("Sistema de Gestão de Clínicas")
root.configure(bg="#96FF00")

# Frame para a busca
search_frame = tk.Frame(root, bg="#96FF00")
search_frame.pack(fill="x")

search_label = tk.Label(search_frame, text="Buscar Paciente:", font=("Arial",12), bg="#96FF00")
search_label.pack(side="left")

search_entry = tk.Entry(search_frame, font=("Arial",12))
search_entry.pack(side="left", fill="x", expand=True)

search_button = tk.Button(search_frame, text="Buscar", command=search_patient, font=("Arial",12,"bold"), bg="#69006A", fg="#ffffff")
search_button.pack(side="left")


# Treeview para exibir os pacientes
tree = ttk.Treeview(root, columns=("id", "nome", "telefone", "email"), show="headings") # Adicionado email
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("telefone", text="Telefone")
tree.heading("email", text="Email") # Cabeçalho do email
tree.pack(fill="both", expand=True, padx=10, pady=5)

# Scrollbar vertical
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(yscrollcommand=vsb.set)

# Botões
button_frame = tk.Frame(root, bg="#96FF00")
button_frame.pack(fill="x")

add_button = tk.Button(button_frame, text="Adicionar", command=add_patient, font=("Arial",12,"bold"), bg="#017553", fg="#ffffff") # Botão de adicionar
add_button.pack(side="left", padx=5)

edit_button = tk.Button(button_frame, text="Editar", command=edit_patient, font=("Arial",12,"bold"), bg="#1F6E03", fg="#ffffff")
edit_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Deletar", command=delete_patient, font=("Arial",12,"bold"), bg="#A30000", fg="#ffffff")
delete_button.pack(side="left")

# Carrega os dados iniciais na Treeview
update_treeview(pacientes)

root.mainloop()