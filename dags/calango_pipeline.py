from airflow.decorators import dag, task
import pendulum
import requests

# Configuração do fuso horário para São Paulo
sao_paulo_tz = pendulum.timezone("America/Sao_Paulo")

@dag(
    dag_id='pipeline_calango_investimentos',
    start_date=pendulum.datetime(2024, 1, 1, tz=sao_paulo_tz),
    schedule=None,
    catchup=False,
    tags=['calango', 'api', 'distribuido']
)
def calango_etl():

    @task()
    def fetch_users():
        response = requests.get('https://fakestoreapi.com/users')
        return response.json()[:10]

    @task()
    def fetch_products():
        response = requests.get('https://fakestoreapi.com/products')
        return response.json()[:10]

    @task()
    def fetch_carts():
        response = requests.get('https://fakestoreapi.com/carts')
        return response.json()[:10]

    @task()
    def load_to_database(users, products, carts):
        print(f"Armazenando no banco: {len(users)} usuários, {len(products)} produtos e {len(carts)} carrinhos.")
        return "Carga concluída com sucesso!"

    # Paralelizando a execução: as três tasks de fetch rodam simultaneamente
    users_data = fetch_users()
    products_data = fetch_products()
    carts_data = fetch_carts()

    # A task de load depende das três anteriores
    load_to_database(users_data, products_data, carts_data)

dag_instance = calango_etl()