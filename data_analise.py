import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importar dados
# file_csv = r"D:\\_tmp\\_md\\tarefas\\estatisticas\\appcons.csv"
file_csv = r"\\vmware-host\Shared Folders\Backup\_tmp\_md\tarefas\estatisticas\appcons.csv"
df = pd.read_csv(file_csv)

# Contar a quantidade de tarefas por tipo
task_type_counts = df['Tipo'].value_counts()

print(task_type_counts)

# Gerar um gráfico de barras
task_type_counts.plot(kind='bar')
plt.title('Quantidade de tarefas por tipo')
plt.xlabel('Tipo de Tarefa')
plt.ylabel('Quantidade')
plt.xticks(rotation=0)
plt.show()

