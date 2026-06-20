import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/tasks"

st.set_page_config(page_title="TaskFlow AI", page_icon="👑", layout="wide")

st.title("👑 TaskFlow Analytics")
st.write("Sistema Inteligente de Gestão e Produtividade.")


st.header("Adicionar Nova Tarefa")
with st.form("new_task_form"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Título da Tarefa")
        priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    with col2:
        status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluída"])
    
    description = st.text_area("Descrição (Opcional)")
    
    submitted = st.form_submit_button("Salvar Tarefa")
    
    if submitted:
        if title:
            payload = {
                "title": title,
                "description": description,
                "priority": priority,
                "status": status
            }
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code in [200, 201]:
                    st.success("Tarefa criada com sucesso!")
                else:
                    st.error(f"Erro ao criar tarefa: {response.text}")
            except Exception as e:
                st.error(f"Erro de conexão com a API: {e}")
        else:
            st.warning("O título da tarefa é obrigatório!")

st.divider()

st.header("Dashboard de Produtividade")

col_atualizar, _ = st.columns([1, 5])
with col_atualizar:
    if st.button("Atualizar Dados 🔄"):
        pass

try:
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        tasks = response.json()
        
        if tasks:
            df = pd.DataFrame(tasks)
            
            col_met1, col_met2, col_met3 = st.columns(3)
            col_met1.metric("Total de Tarefas", len(df))
            col_met2.metric("Concluídas ✅", len(df[df['status'] == 'Concluída']))
            col_met3.metric("Pendentes ⏳", len(df[df['status'] == 'Pendente']))
            
            st.subheader("Análise Visual")
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.write("Distribuição por Status")
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts, color="#22c55e")
                
            with col_graf2:
                st.write("Distribuição por Prioridade")
                priority_counts = df['priority'].value_counts()
                st.bar_chart(priority_counts, color="#3b82f6")
            
            st.subheader("Histórico de Tarefas")
            st.dataframe(df[['id', 'title', 'priority', 'status', 'created_at']], use_container_width=True)
            
        else:
            st.info("Nenhuma tarefa cadastrada ainda. Use o formulário acima para começar!")
    else:
        st.error("Falha ao buscar dados da API.")
        
except Exception as e:
    st.error(f"A API não está respondendo. Certifique-se de que o Uvicorn/Render está rodando. Detalhes do erro: {e}")