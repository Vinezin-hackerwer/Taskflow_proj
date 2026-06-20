import streamlit as st
import requests
import pandas as pd

API_URL = "https://taskflow-proj.onrender.com/items" 

st.set_page_config(page_title="TaskFlow ", page_icon="👑", layout="wide")

def get_tasks():
    """Puxa todas as tarefas da API"""
    try:
        response = requests.get(f"{API_URL}/") 
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                st.error("A API retornou um formato inesperado.")
                return []
        else:
            st.error("Erro ao buscar tarefas do banco de dados.")
            return []
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar à API. Verifique se o Uvicorn ou o Render estão rodando.")
        return []

def create_task(data):
    """Envia uma nova tarefa para a API"""
    try:
        response = requests.post(f"{API_URL}/", json=data)
        return response.status_code in [200, 201]
    except Exception as e:
        st.error(f"Erro ao criar tarefa: {e}")
        return False

def delete_task(task_id):
    """Deleta uma tarefa específica via API"""
    try:
        response = requests.delete(f"{API_URL}/{task_id}")
        return response.status_code == 200
    except Exception as e:
        st.error(f"Erro ao deletar tarefa: {e}")
        return False

st.title("👑 TaskFlow Analytics")
st.markdown("Sistema Inteligente de Gestão e Produtividade.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Nova Tarefa")
    with st.form("form_nova_tarefa", clear_on_submit=True):
        titulo = st.text_input("Título da Tarefa *")
        descricao = st.text_area("Descrição (Opcional)")
        prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
        status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluída"])
        
        submit = st.form_submit_button("Adicionar Tarefa ➕")
        
        if submit:
            if not titulo:
                st.warning("O título é obrigatório!")
            else:
                nova_tarefa = {
                    "title": titulo,
                    "description": descricao,
                    "priority": prioridade,
                    "status": status
                }
                if create_task(nova_tarefa):
                    st.success("Tarefa adicionada com sucesso!")
                    st.rerun() 

with col2:
    st.header("Dashboard de Produtividade")
    
    tarefas = get_tasks()
    

    if tarefas:
        df = pd.DataFrame(tarefas)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total", len(df))
        m2.metric("Concluídas ✅", len(df[df['status'] == 'Concluída']))
        m3.metric("Pendentes ⏳", len(df[df['status'] != 'Concluída']))
        
        st.write("### Suas Tarefas")
        st.dataframe(
            df[['id', 'title', 'priority', 'status']], 
            use_container_width=True,
            hide_index=True
        )

        st.write("### Gerenciar Tarefas")
        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
            opcoes_delete = {f"{t['id']} - {t['title']}": t['id'] for t in tarefas}
            tarefa_para_deletar = st.selectbox("Selecione uma tarefa para remover:", options=list(opcoes_delete.keys()))
        
        with del_col2:
            st.write("") 
            st.write("")
            if st.button("Deletar 🗑️", type="primary"):
                id_alvo = opcoes_delete[tarefa_para_deletar]
                if delete_task(id_alvo):
                    st.success("Tarefa removida!")
                    st.rerun()
    else:
        st.info("Nenhuma tarefa encontrada. Comece adicionando uma ao lado!")
