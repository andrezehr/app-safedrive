import streamlit as st

# Configuração da Página
st.set_page_config(page_title="SafeDrive Brasil", page_icon="🛡️", layout="centered")

# Inicialização de variáveis de sessão
if 'gramas_alcool' not in st.session_state:
    st.session_state.gramas_alcool = 0.0
if 'copos_agua' not in st.session_state:
    st.session_state.copos_agua = 0
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Dicionário de Bebidas (Teor Alcoólico e Volume em ml)
BEBIDAS = {
    "Cerveja (Lata/Long Neck)": [0.05, 350],
    "Cerveja Artesanal (IPA)": [0.08, 330],
    "Chope (Tulipa)": [0.048, 300],
    "Vinho (Taça)": [0.12, 150],
    "Espumante (Taça)": [0.12, 125],
    "Cachaça/Vodka/Gin (Dose)": [0.40, 50],
    "Whiskey (Dose)": [0.43, 50],
    "Tequila (Shot)": [0.40, 40],
    "Caipirinha": [0.18, 200],
    "Gin Tônica": [0.10, 250],
    "Licor (Cálice)": [0.20, 30]
}

# --- SIDEBAR: CONFIGURAÇÕES E PERFIL ---
st.sidebar.header("👤 Seu Perfil")
peso = st.sidebar.number_input("Peso (kg):", min_value=30, value=75)
sexo = st.sidebar.radio("Sexo Biológico:", ("Masculino", "Feminino"))
fator_r = 0.68 if sexo == "Masculino" else 0.55

st.sidebar.divider()
st.sidebar.header("🛡️ Segurança")
contato_nome = st.sidebar.text_input("Nome do Anjo da Guarda:")
contato_tel = st.sidebar.text_input("WhatsApp (ex: 5511999999999):")

if st.sidebar.button("🗑️ Reiniciar Sessão / Sóbrio"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🛡️ SafeDrive Brasil")
st.subheader("Gerencie seu consumo e proteja sua vida (e seu bolso).")

# 1. ENTRADA DE DADOS RÁPIDA
st.markdown("### ➕ Adicionar ao seu Diário")
c_bebe, c_agua = st.columns(2)

with c_bebe:
    bebida_sel = st.selectbox("O que você está bebendo?", list(BEBIDAS.keys()))
    if st.button("🍻 Registrar Bebida"):
        teor, vol = BEBIDAS[bebida_sel]
        st.session_state.gramas_alcool += (vol * teor * 0.8)
        st.session_state.historico.append(bebida_sel)
        st.rerun()

with c_agua:
    st.write("Hidratação:")
    if st.button("💧 Beber Água (200ml)"):
        st.session_state.copos_agua += 1
        st.rerun()

# Interruptor de Estômago
estomago_cheio = st.toggle("🍽️ Comi algo recentemente / Estou jantando", value=False)
ajuste_estomago = 0.7 if estomago_cheio else 1.0

# --- CÁLCULOS ---
bac_sangue = (st.session_state.gramas_alcool * ajuste_estomago) / (peso * fator_r)
bafometro = bac_sangue / 2 
tempo_horas = bac_sangue / 0.15

# --- DASHBOARD DE RESULTADOS ---
st.divider()

if bac_sangue > 0:
    # Status Dinâmico
    if bac_sangue < 0.3:
        st.info("🍃 **Status:** Já está relaxando... Curta com moderação!")
    elif bac_sangue < 0.5:
        st.warning("⚠️ **Status:** Opa, hora de ir mais devagar!")
    else:
        st.error("🚫 **Status:** VOCÊ NÃO PODE DIRIGIR!")

    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("No Sangue", f"{bac_sangue:.2f} g/L")
    m2.metric("Bafômetro (est.)", f"{bafometro:.2f} mg/L")
    m3.metric("Tempo p/ Zerar", f"{int(tempo_horas)}h {int((tempo_horas%1)*60)}min")

    # CONSCIENTIZAÇÃO FINANCEIRA
    if bafometro > 0.04:
        with st.expander("💸 VEJA O CUSTO DE DIRIGIR AGORA"):
            st.write("🔴 **Multa:** R$ 2.934,70")
            st.write("🔴 **Penalidade:** Suspensão da CNH por 12 meses.")
            if bafometro >= 0.34:
                st.error("👮 **CRIME DE TRÂNSITO:** Risco de prisão em flagrante!")

    # BOTÕES DE AÇÃO (SEGURANÇA E TRANSPORTE)
    st.markdown("### 🚗 Alternativas para Voltar em Segurança")
    
    col_uber, col_99, col_anjo = st.columns(3)
    
    with col_uber:
        # Deep links para abrir apps no celular
        st.link_button("🚕 Uber", "https://m.uber.com/ul/?action=setPickup")
    
    with col_99:
        st.link_button("🚖 99", "https://99app.com/")
        
    with col_anjo:
        if contato_tel:
            msg = f"Oi {contato_nome}, o SafeDrive avisou que meu nível de álcool está alto ({bac_sangue:.2f}g/L). Pode me ajudar com uma carona?"
            link = f"https://wa.me/{contato_tel}?text={msg.replace(' ', '%20')}"
            st.link_button("😇 Anjo da Guarda", link)
        else:
            st.caption("Configure o Anjo na lateral")

else:
    st.success("✅ Você está totalmente sóbrio.")

# Barra de Hidratação
if len(st.session_state.historico) > 0:
    st.divider()
    progresso = min(st.session_state.copos_agua / len(st.session_state.historico), 1.0)
    st.write(f"Meta de Hidratação: {st.session_state.copos_agua}/{len(st.session_state.historico)} copos")
    st.progress(progresso)

st.divider()
st.caption("⚠️ **Atenção:** Simulador baseado em médias estatísticas. A tolerância da Lei Seca é ZERO. Se beber, não dirija.")