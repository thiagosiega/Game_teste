import os

FILE_LOGS_ERROR = "Logs/LogsError.txt"

def pasta_logs():
    try:
        os.makedirs("Logs")
    except FileExistsError:
        pass

def criar_log_erro(conteudo):
    separador = "=" * 60
    try:
        with open(FILE_LOGS_ERROR, "a") as file:
            file.write(f"{separador}\n{conteudo}\n")
        return True
    except Exception as e:
        print(f"Erro ao criar log de erro: {e}")
        return False

def main(Titulo, mensagem, descricao):
    # Verifica se o Titulo e a mensagem são strings
    if not isinstance(Titulo, str) or not isinstance(mensagem, str):
        print("Título e mensagem devem ser strings.")
        return False

    pasta_logs()
    
    # Cria o conteúdo do log de erro
    conteudo = f"Título: {Titulo}\nMensagem: {mensagem}\nDescrição: {descricao}"
    
    # Grava o log de erro
    if criar_log_erro(conteudo):
        print("Log de erro criado com sucesso.")
    else:
        print("Falha ao criar o log de erro.")
        
if __name__ == "__main__":
    Titulo = "Erro"
    mensagem = "Erro ao tentar abrir o arquivo"
    descricao = "O arquivo não foi encontrado"
    main(Titulo, mensagem, descricao)
