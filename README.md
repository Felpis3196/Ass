# 📦 Anticipatory Shipping Simulation

Este projeto foi criado com o intuito de estudar e simular de forma simplificada o processo de **Anticipatory Shipment System (ASS)** utilizado pela Amazon em grandes metrópoles.  

A ideia central do sistema é **antecipar a logística** de determinados produtos para agilizar a entrega, deixando-os:  
- Pré-separados,  
- Pré-embalados, ou até mesmo  
- Enviados para o **centro logístico mais próximo do cliente** antes mesmo da finalização da compra.  

Tudo isso é feito com base em análises de **comportamento do usuário**, como:  
- Tempo gasto visualizando o item,  
- Tempo em que o item permanece no carrinho,  
- Ações realizadas recentemente,  
- Histórico de busca e interesse,  
- Avaliações e reviews pesquisados.  

## 🚀 Objetivo
O projeto utiliza **IA com Random Forest** para prever a probabilidade de um usuário realizar uma compra, simulando decisões logísticas baseadas em diferentes níveis de confiança:  

- **> 95% + item no carrinho** → Enviar imediatamente  
- **> 85%** → Pré-reservar em hub logístico próximo  
- **<= 85%** → Aguardar decisão do usuário  

Com isso, é possível demonstrar como um sistema desse tipo **economiza milhões em operações logísticas**, reduzindo tempo de entrega e otimizando estoques.

## 🔮 Futuro
Uma possível evolução para este projeto é conectar o modelo a uma **API real de e-commerce**, de forma a alimentar os dados do sistema continuamente. Assim, o modelo ficaria cada vez mais preciso, aprendendo com os novos padrões de comportamento de compra.

## 🛠️ Tecnologias Utilizadas
- **Python 3**  
- **Pandas** para manipulação de dados  
- **Scikit-learn** para machine learning (Random Forest)  
- **Joblib** para salvar o modelo  
- **UUID** para rastreamento de previsões  

## 📂 Estrutura da Simulação
1. Leitura de dados de treino (`dados_treino.csv`)  
2. Leitura de dados fictícios de usuários (`dados_usuarios.json`)  
3. Treinamento e exportação do modelo  
4. Previsões com base nos novos dados  
5. Geração de arquivos CSV:  
   - `resultados_predicoes.csv` → Resultado completo das previsões  
   - `acoes_logisticas.csv` → Apenas as ações logísticas relevantes  

## 📊 Exemplo de Saída
| prediction_id | item_name  | decisão        | probabilidade (%) | ação logística       | prioridade | hub destino |
|---------------|------------|----------------|-------------------|----------------------|------------|-------------|
| 123e4567...   | Fone XYZ   | Compraria      | 96.21%            | Enviar imediatamente | Alta       | Centro SP   |
| 89ab1234...   | Mouse ABC  | Não compraria  | 42.15%            | Aguardar             | Baixa      | Centro RJ   |
| 456cd789...   | Livro DEF  | Compraria      | 87.03%            | Pré-reservar em hub  | Média      | Centro MG   |

---

👉 Este repositório é apenas uma **prova de conceito acadêmica**, não um sistema de produção.  
