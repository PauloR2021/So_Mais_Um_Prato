from dotenv import load_dotenv
import pyodbc
import os

def conexao():
    try:
        
        load_dotenv()
        
        DRIVER = os.getenv("MYSQL_DRIVER")
        SERVER = os.getenv("MYSQL_HOST")
        DATABASE = os.getenv("MYSQL_DB")
        USER = os.getenv("MYSQL_USER")
        PSWD = os.getenv("MYSQL_PASSWORD")
        
        conexao_db = pyodbc.connect(
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USER};PWD={PSWD};'
        )
    
    except Exception as e:
        print(str(e))
    return conexao_db

def login_usuario(email,senha):
    
    try:
        
        cursor = conexao().cursor()
        
        string_sql = """
                    SELECT * FROM PROJETOS_PYTHON.dbo.PROJETO_SO_MAIS_UM_PRATO_LOGIN
                    WHERE EMAIL = ? AND SENHA = ?
                """
        cursor.execute(string_sql, (email, senha))   
        row = cursor.fetchone()
        
        if row:
            columns = [column[0] for column in cursor.description]
            usuario = dict(zip(columns,row))
        else:
            usuario = None
             
        cursor.close()
        conexao.close()

    except Exception as e:
        print(e)
    
    return usuario
    
    
def todas_receitas():
    cursor = conexao().cursor()
    string_sql = "SELECT * FROM PROJETOS_PYTHON.dbo.SO_MAIS_UM_PRATO_RECEITAS;"
    cursor.execute(string_sql)
    receitas = cursor.fetchall()
    
    return receitas

def todas_receitas_busca(busca:str):
    cursor = conexao().cursor()
    string_sql = "SELECT * FROM PROJETOS_PYTHON.dbo.SO_MAIS_UM_PRATO_RECEITAs WHERE NOME_RECEITA LIKE '%?%;"
    cursor.execute(string_sql(busca))
    receitas = cursor.fetchall()
    
    return receitas
    
def todas_receitas_buscar_id(id:int):
    conn = conexao()
    cursor = conn.cursor()
    string_sql = "SELECT * FROM PROJETOS_PYTHON.dbo.SO_MAIS_UM_PRATO_RECEITAs WHERE ID = ?;"
    cursor.execute(string_sql, (id,))
    row = cursor.fetchone()

    if row is None:
        return None

    # Pegando os nomes das colunas
    columns = [column[0] for column in cursor.description]

    # Convertendo a tupla para dicionário
    receita = dict(zip(columns, row))

    
    return receita

def cadastrar_receitas(nome:str,ingredientes:str,tempo:int,porcoes:int,preparo:str,imagem:str):
    try:
        
        cursor = conexao().cursor()
        
        string_sql =f"""
                        INSERT INTO PROJETOS_PYTHON.dbo.SO_MAIS_UM_PRATO_RECEITAS
                        (NOME_RECEITA, INGREDIENTES, TEMPO_PREPARO, PORCOES, MODO_PREPARO, IMAGEM)
                        VALUES('{nome}', '{ingredientes}', {tempo}, {porcoes}, '{preparo}', '{imagem}');
                    """
        cursor.execute(string_sql)
        cursor.commit()
        
        cursor.close()
        conexao().close()
    except Exception as e :
        print(e)
        


if __name__ == "__main__":
    teste = todas_receitas_buscar_id(1)
    
    print(teste)
