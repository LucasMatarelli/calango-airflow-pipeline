# 🦎 Calango Investimentos: Pipeline de Dados com Airflow Distribuído

Este projeto é uma simulação de ambiente de Engenharia de Dados corporativo construído para a **Calango Investimentos**, uma fintech em expansão após a aquisição de um novo marketplace. 

O objetivo principal desta arquitetura é substituir um MVP antigo por um pipeline altamente escalável, utilizando orquestração distribuída para extrair dados em paralelo de uma API (usuários, produtos e carrinhos) e simulando a carga em um banco de dados relacional.

## 🛠️ Arquitetura e Tecnologias

* **Apache Airflow:** Orquestração do pipeline via TaskFlow API (`@dag`, `@task`).
* **Celery Executor:** Gerenciamento distribuído de tarefas.
* **Redis:** Message Broker para comunicação entre o Scheduler e os Workers.
* **PostgreSQL:** Banco de dados de metadados do Airflow.
* **Docker & Docker Compose:** Containerização e gerenciamento dinâmico de infraestrutura.
* **Flower:** Monitoramento em tempo real da saúde dos Workers.

## 🚀 Estrutura da DAG e Execução

O pipeline foi configurado utilizando o fuso horário `America/Sao_Paulo` (via Pendulum) e paraleliza o consumo dos seguintes endpoints da FakeStore API:
1. `/users`
2. `/products`
3. `/carts`

Abaixo, a comprovação do sucesso da execução da DAG, onde as 3 tarefas de extração ocorrem simultaneamente antes de acionar a carga (`load_to_database`):

### Grid View (Sucesso das Tarefas)
![Execução com Sucesso](airflow2.png)
*Execução registrada sem falhas na esteira de dados.*

### Graph View (Paralelismo)
![Grafo da DAG](airflow3.png)
*O fluxo de dependências demonstrando a paralelização imposta pelos requisitos de negócio.*

## ⚖️ Testes de Escala da Infraestrutura (Workers Dinâmicos)

Para garantir que o ambiente atende à alta volumetria do novo marketplace, a infraestrutura foi submetida a testes de estresse e escalabilidade dinâmica utilizando a flag `--scale` do Docker Compose.

**1. Ambiente Inicial (3 Workers)**
A arquitetura foi levantada inicialmente fixando 3 nós de processamento ativos para consumir a fila do Celery.
![3 Workers Ativos](airflow1.png)

**2. Redução Dinâmica (2 Workers)**
Após testes de sobrecarga com 5 workers, a infraestrutura foi reduzida graciosamente para 2 workers sem impacto aos serviços principais (Scheduler/Webserver) ou interrupção do sistema.
![2 Workers Ativos](airflow4.png)

---
*Projeto desenvolvido como parte de simulação arquitetural de Engenharia de Dados.*
