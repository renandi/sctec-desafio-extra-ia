#!/usr/bin/env python
# coding: utf-8

# # Importação das bibliotecas

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# # Configuração global para os gráficos

# In[3]:


# Configuração para os gráficos
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'

plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12


# # Carregando dataframe e verificando tipos de dados

# In[4]:


df = pd.read_csv("ncr_ride_bookings.csv")
df.head()


# In[5]:


# Verificando mais informações sobre as colunas
df.info()


# In[6]:


# Apagar colunas que não serão úteis nessa análise
df.drop(["Booking ID", "Customer ID", "Pickup Location", "Drop Location"], axis=1, inplace=True)


# In[7]:


# Obtendo mais informações sobre colunas numéricas
df.describe()


# In[8]:


# Criar coluna com formato full datetime
df["Full Datetime"] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), format='%Y-%m-%d %H:%M:%S')
df["Full Datetime"].head()


# In[9]:


print("Data mínima: ", df["Full Datetime"].min(), "\nData máxima:", df["Full Datetime"].max())


# # Explorando os dados

# ## Distribuição temporal das corridas

# ### Distribuição de corridas por mês

# In[10]:


sns.histplot(df["Full Datetime"].dt.month, discrete=True)
plt.title("Número de corridas chamadas por mês")
plt.xlabel("Mês")
plt.xticks(range(1,13))
plt.ylabel("Número de corridas")
plt.savefig('images/rides-by-month.png')
plt.show()


# ### Distribuição de corridas ao longo do mês

# In[11]:


sns.histplot(df["Full Datetime"].dt.day, discrete=True)
plt.title("Número de corridas chamadas por dia do mês")
plt.xlabel("Dia do mês")
plt.xticks(range(1,32,2))
plt.ylabel("Número de corridas")
plt.savefig('images/rides-by-day-of-month.png')
plt.show()


# In[12]:


sns.histplot(df["Full Datetime"].dt.dayofweek, discrete=True)
plt.title("Número de corridas chamadas por dia da semana")
plt.xlabel("Dia da semana")
plt.ylabel("Número de corridas")
plt.savefig('images/rides-by-dayofweek.png')
plt.show()


# ### Distribuição de corridas por hora do dia

# In[13]:


# Plotar numero de corridas chamadas por horas do dia

sns.histplot(df["Full Datetime"].dt.hour, discrete=True)
plt.title("Número de corridas chamadas por hora do dia")
plt.xlabel("Hora")
plt.xticks(range(0,24,2))
plt.ylabel("Número de corridas")
plt.savefig('images/rides-by-hour.png')
plt.show()


# ## Explorando status de corridas e cancelamentos

# In[14]:


df["Booking Status"].value_counts()


# ### Analisando proporção de cancelamentos

# In[15]:


# Distribuição de status das corridas completadas e canceladas

status_counts = df["Booking Status"].value_counts()
status_labels_pt = ["Completa", "Canceladas pelo motorista", "Motorista não encontrado", "Canceladas pelo cliente", "Incompletas"]

plt.figure(figsize=(5, 5))
plt.pie(
    status_counts,
    labels = status_labels_pt,
    autopct='%1.1f%%',
    colors=['#2ecc71', '#e74c3c', '#3498db', '#f1c40f', '#999']
)
plt.title("Proporção de Status das Corridas")
plt.savefig("images/pie-chart-status.png")
plt.show()


# ### Verificando relação entre horário e proporção de cancelamentos

# In[16]:


# Verificar se há um horário onde os clientes cancelam mais

total_por_hora = df["Full Datetime"].dt.hour.value_counts().sort_index()

canceladas_por_clientes = df[df["Booking Status"] == "Cancelled by Customer"]

canceladas_por_hora_por_clientes = canceladas_por_clientes["Full Datetime"].dt.hour.value_counts().sort_index()

proporcao_cancelamento = canceladas_por_hora_por_clientes / total_por_hora *100

sns.barplot(x=proporcao_cancelamento.index, y = proporcao_cancelamento.values)
plt.title("Porcentagem de cancelamento por hora do dia")
plt.xlabel("Hora do dia")
plt.xticks(range(24))
plt.ylabel("Porcentagem de cancelamento (%)")

plt.savefig("images/cancel-percent-per-hour.png")
plt.show()


# ### Verificando relação entre tempo de espera e cancelamento

# In[49]:


# Verificar relação entre tempo de chegada do motorista e cancelamentos por clientes

df_comparacao = df[df["Booking Status"].isin(["Completed", "Cancelled by Customer", "Cancelled by Driver"])]

sns.boxplot(data=df_comparacao, x="Booking Status", y="Avg VTAT", palette="Set2", hue="Booking Status")
plt.title("Tempo de Chegada do Motorista vs. Status da Corrida")
plt.xlabel("Status da Corrida")
plt.ylabel("Tempo de Chegada (Minutos)")

plt.savefig("images/avtat-box.png")
plt.show()


# ## Correlação entre variáveis numéricas

# In[59]:


df_completas = df[df["Booking Status"] == "Completed"]

df_corr = df_completas[["Avg VTAT", "Avg CTAT", "Booking Value", "Ride Distance", "Driver Ratings", "Customer Rating"]]

corr = df_corr.corr()

corr


# In[64]:


# Remover diagonal e triangulo superior para melhor visualização no heatmap

tri = corr.where(np.tril(np.ones(corr.shape), k=0).astype(bool))
tri.dropna(how='all').dropna(axis=1, how='all')
tri.replace(1, np.nan, inplace=True)


# In[68]:


sns.heatmap(
    tri, 
    annot=tri, 
    fmt=".5f", 
    linewidths=.5,
    # vmin=tri.min().min(), # O mínimo real dos seus dados
    # vmax=tri.max().max(), # O máximo real dos seus dados
    cmap="viridis"
)
plt.title("Correlação entre dados numéricos")

plt.savefig("images/corr-heatmap.png")
plt.show()