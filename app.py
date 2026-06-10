import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="centered")
st.title("📊 Dashboard de Apoio à Construção do MindQuest")

#Tentativa de mudar um pouco a aparência do Dashboard pra ficar com a carinha do MindQuest

st.markdown("""
### 🎮 Transformando o uso consciente da tecnologia em uma jornada de evolução pessoal

Este dashboard foi utilizado para analisar padrões de comportamento digital
e auxiliar no desenvolvimento do MindQuest.
""")

#Calculos dos indicadores


mental = pd.read_csv("https://drive.google.com/uc?id=1azYVj-tUuEwJZAATnEx6RVUbsUQvqRcc")
detox = pd.read_csv("https://drive.google.com/uc?id=1vqszv2OhjPwtDc62sod9FtIaA-MfA6YF")
prod = pd.read_csv("https://drive.google.com/uc?id=1Pq6y0KCli6u-YWIKskCgkBnOqvSCrNol")
#testando colocar novo gráfico
produtividade = pd.read_csv("https://drive.google.com/uc?id=1EapdIQkSn62CuTEfAd1F_tvmtxzkOU7f")
for col in [
    "daily_screen_time",
    "study_hours",
    "sleep_hours"
]:
    produtividade[col] = pd.to_numeric(
        produtividade[col],
        errors="coerce")
produtividade["Faixa Etária"] = pd.cut(
    produtividade["age"],
    bins=[0, 19, 35, 59, 120],
    labels=[
        "Adolescente",
        "Jovem Adulto",
        "Adulto",
        "Idoso"]
)
#aqui já coloquei o link

idade_pt = {
    "Teen": "Adolescente",
    "Young Adult": "Jovem Adulto",
    "Adult": "Adulto",
    "Senior": "Idoso"}
detox["age_group"] = detox["age_group"].replace(idade_pt)
detox["successful_detox"] = detox["successful_detox"].map(
    lambda x: "Sucesso" if str(x).lower() in ["true", "1", "sim"] else "Falha")

#Mais uma nova alteração
produtividade_group = (
    produtividade.groupby("Faixa Etária")
    [
        [
            "daily_screen_time",
            "study_hours",
            "sleep_hours"]
    ]
    .mean()
    .reset_index()
)
produtividade_group = produtividade_group.rename(columns={
    "daily_screen_time": "Tempo de Tela Diário",
    "study_hours": "Horas de Estudo",
    "sleep_hours": "Horas de Sono"}
)
#acabei aqui

relapse_age = detox.groupby("age_group")["relapse_probability"].mean().reset_index()
relapse_platform = detox.groupby("platform")["relapse_probability"].mean().reset_index()
media_relapse = detox["relapse_probability"].mean()
plataforma_critica = relapse_platform.loc[
    relapse_platform["relapse_probability"].idxmax(),"platform"]
plataforma_mais_usada = detox["platform"].mode()[0]
faixa_critica = relapse_age.loc[
    relapse_age["relapse_probability"].idxmax(),"age_group"]
col1, col2, col3, col4 = st.columns([4])
col1.metric(
    "📉 Recaída Média",
    f"{media_relapse:.0%}")
col2.metric( 
    "📱 Maior Recaída",
    plataforma_critica)
col3.metric(
    "📊 Mais Utilizada",
    plataforma_mais_usada)
with col4:
    st.markdown("""
    <div style="text-align:center;">
        <p style="font-size:14px; margin-bottom:5px;">
            👥 Faixa Mais Vulnerável
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:center;">
            <h3>{faixa_critica}</h3>
        </div>
        """,
        unsafe_allow_html=True)

#Inserindo o novo gráfico logo no início
st.divider()

#primeiro gráfico
st.header("⏳ Produtividade e Hábitos por Faixa Etária")
fig0 = px.bar(
    produtividade_group,
    x="Faixa Etária",
    y=[
        "Tempo de Tela Diário",
        "Horas de Estudo",
        "Horas de Sono"
    ],
    barmode="group",
    title="Tempo de Tela, Estudo e Sono por Faixa Etária",
    labels={
        "value": "Quantidade de Horas",
        "variable": "Indicador"}
)
st.plotly_chart(fig0, use_container_width=True)
st.info(
    "💡 Insight: A comparação entre tempo de tela, estudo e sono permite identificar padrões de equilíbrio digital entre as diferentes faixas etárias.")
#finalizei

st.divider()

#segundo gráfico
st.header("📊 Distribuição de uso por plataforma")
uso_plataforma = detox["platform"].value_counts().reset_index()
uso_plataforma.columns = ["platform", "usuarios"]
fig_pizza = px.pie(
    uso_plataforma,
    names="platform",
    values="usuarios",
    title="Plataformas mais utilizadas")
st.plotly_chart(fig_pizza, use_container_width=True)
st.info(
    f"💡 Insight: {plataforma_mais_usada} foi a plataforma mais utilizada entre os usuários analisados.")

st.divider()

#terceiro gráfico
st.header("📱 Saúde mental por plataforma")
platform_group = mental.groupby("platform")[["anxiety_score", "stress_level", "loneliness_index", "depression_score"]].mean().reset_index()
platform_group = platform_group.rename(columns={
    "anxiety_score": "Pontuação de Ansiedade",
    "stress_level": "Nível de Estresse",
    "loneliness_index": "Índice de Solidão",
    "depression_score": "Pontuação de Depressão"})
fig1 = px.bar(
    platform_group,
    y="platform",
    x=[
        "Pontuação de Ansiedade",
        "Nível de Estresse",
        "Índice de Solidão",
        "Pontuação de Depressão"
    ],
    orientation="h",
    title="Indicadores de Saúde Mental por Plataforma",
    barmode="group",
    labels={
        "platform": "Plataforma",
        "value": "Valor",
        "variable": "Indicador"
    }
)
st.plotly_chart(fig1, use_container_width=True)

#Estou colocando mais Insights, para mostrar conhecimento além dos gráficos
maior_ansiedade = platform_group.loc[
    platform_group["Pontuação de Ansiedade"].idxmax(),
    "platform"
]
st.info(f"💡 Insight: {maior_ansiedade} apresentou os maiores indicadores de impacto emocional, destacando-se principalmente na média de ansiedade.")

#Acaba aqui

st.divider()

#quarto gráfico
st.header("🧪 Sucesso vs Falha nas tentativas de detox")
detox_group = detox.groupby(["detox_attempts", "successful_detox"]).size().reset_index(name="count")
fig3 = px.bar(
    detox_group,
    x="detox_attempts",
    y="count",
    color="successful_detox",
    title="Tentativas de Detox x Resultado",
    labels={
        "detox_attempts": "Número de Tentativas",
        "count": "Quantidade de Usuários",
        "successful_detox": "Resultado"
    }
)

st.plotly_chart(fig3, use_container_width=True)

#Mais um Insight

st.info(
    "💡 Insight: O número de tentativas influencia diretamente as chances de sucesso no detox digital.")

#Pronto

st.divider()

#quinto gráfico
st.header("🔁 Probabilidade de recaída por idade")

fig2 = px.bar(
    relapse_age.sort_values("relapse_probability"),
    y="age_group",
    x="relapse_probability",
    orientation="h",
    title="Probabilidade de Recaída por Faixa Etária",
    labels={
        "age_group": "Faixa Etária",
        "relapse_probability": "Probabilidade de Recaída"
    }
)

st.plotly_chart(fig2, use_container_width=True)
maior_relapse = relapse_age.loc[
    relapse_age["relapse_probability"].idxmax(),
    "age_group"
]
st.info(
    f"💡 Insight: A faixa etária {maior_relapse} apresentou a maior probabilidade média de recaída.")
st.divider()

#sexto gráfico
st.header("👥📈 Sucesso de detox por faixa etária")
age_success = detox.groupby(["age_group", "successful_detox"]).size().reset_index(name="count")
fig4 = px.bar(
    age_success,
    y="age_group",
    x="count",
    color="successful_detox",
    orientation="h",
    title="Sucesso e Falha no Detox por Faixa Etária",
    labels={
        "age_group": "Faixa Etária",
        "count": "Quantidade de Usuários",
        "successful_detox": "Resultado"
    }
)
st.plotly_chart(fig4, use_container_width=True)
sucesso_por_idade = age_success[
    age_success["successful_detox"] == "Sucesso"]
melhor_faixa = sucesso_por_idade.loc[
    sucesso_por_idade["count"].idxmax(),
    "age_group"]
st.info(f"💡 Insight: A faixa etária {melhor_faixa} apresentou a maior quantidade de casos de sucesso no detox digital.")
st.divider()

#sétimo gráfico
st.header("📉 Recaída média por plataforma")

fig5 = px.bar(
    relapse_platform.sort_values("relapse_probability"),
    x="platform",
    y="relapse_probability",
    title="Probabilidade Média de Recaída por Plataforma",
    labels={
        "platform": "Plataforma",
        "relapse_probability": "Probabilidade de Recaída"
    }
)
st.plotly_chart(fig5, use_container_width=True)
media = relapse_platform["relapse_probability"].mean()
st.info(f"💡 Insight: {plataforma_critica} apresentou a maior probabilidade média de recaída, reforçando a importância de mecanismos de acompanhamento contínuo para usuários dessa plataforma.")
st.divider()
st.subheader("🧠 Insight")
st.write(f"Média global de recaída: {media:.2f}")
if 0.45 < media < 0.55:
    st.warning("A recaída é aproximadamente 50% → comportamento sistêmico.")
st.divider()
st.success("""
🎯 Conclusão

Os dados indicam que padrões de uso excessivo das redes sociais estão associados
a maiores índices de estresse, depressão e recaída em processos de detox digital.

Esses resultados reforçam a necessidade de soluções que promovam hábitos digitais
mais saudáveis, motivação contínua e acompanhamento personalizado, fundamentos
que deram origem ao MindQuest.
""")
