import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# ---------- Carregando dados ------------
tabela = pd.read_csv("vendas.csv")


# --------- Tratamento / Criação de métricas ------------
tabela["faturamento"] = tabela["preco"] * tabela["quantidade"]


# ---------- Análises ----------------
cidade = (
    tabela.groupby("cidade")["faturamento"]
    .sum().round(2)
    .sort_values(ascending=False)
)

produto = (
    tabela.groupby("produto")["faturamento"]
    .sum().round(2)
    .sort_values(ascending=False)
)

categoria = (
    tabela.groupby("categoria")["faturamento"]
    .sum().round(2)
    .sort_values(ascending=False)
)

tabela["data_pedido"] = pd.to_datetime(tabela["data_pedido"])
tabela["mes_num"] = tabela["data_pedido"].dt.month
tabela["mes_nome"] = tabela["data_pedido"].dt.strftime("%b")

faturamento_mes = (
    tabela.groupby(["mes_num", "mes_nome"])["faturamento"]
    .sum()
    .reset_index()
    .sort_values("mes_num")
)

mes_top = faturamento_mes.loc[faturamento_mes["faturamento"].idxmax()]
total = tabela["faturamento"].sum().round(2)


# ------------ Gráficos -----------
def fmt_reais(x, pos):
    return f"R${x/1000:.0f}k"

fig, axes = plt.subplots(1, 4, figsize=(18, 5))
fig.suptitle("Análise de Vendas - E-commerce", fontsize=14, fontweight="bold")

# Top 5 Produtos
axes[0].set_title("Top 5 Produtos por Faturamento")
produto.head(5).plot(kind="bar", ax=axes[0], color="steelblue")
axes[0].set_xlabel("Produto")
axes[0].set_ylabel("Faturamento")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
axes[0].tick_params(axis="x", rotation=45)

# Cidades
axes[1].set_title("Faturamento por Cidade")
cidade.plot(kind="bar", ax=axes[1], color="darkorange")
axes[1].set_xlabel("Cidade")
axes[1].set_ylabel("Faturamento")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
axes[1].tick_params(axis="x", rotation=45)

# Categorias
axes[2].set_title("Faturamento por Categoria")
categoria.plot(kind="bar", ax=axes[2], color="seagreen")
axes[2].set_xlabel("Categoria")
axes[2].set_ylabel("Faturamento")
axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
axes[2].tick_params(axis="x", rotation=45)

# Evolução mensal
axes[3].set_title("Evolução do Faturamento Mensal")
axes[3].plot(faturamento_mes["mes_nome"], faturamento_mes["faturamento"],
             marker="o", color="purple", linewidth=2)
axes[3].set_xlabel("Mês")
axes[3].set_ylabel("Faturamento")
axes[3].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_reais))
axes[3].tick_params(axis="x", rotation=45)

plt.tight_layout()

# Salva o dashboard como imagem (usado no README do GitHub)
plt.savefig("dashboard_vendas.png", dpi=150, bbox_inches="tight")
plt.show()


# --------- Insights ---------
print(f"Faturamento total: R$ {total:,.2f}")
print(f"Produto com maior faturamento: {produto.index[0]} — R$ {produto.iloc[0]:,.2f}")
print(f"Cidade com maior faturamento: {cidade.index[0]} — R$ {cidade.iloc[0]:,.2f}")
print(f"Categoria mais lucrativa: {categoria.index[0]} — R$ {categoria.iloc[0]:,.2f}")
print(f"Mês com maior faturamento: {mes_top['mes_nome']} — R$ {mes_top['faturamento']:,.2f}")
