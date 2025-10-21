# language: pt
Funcionalidade: API de Usuários da Plataforma ConectaVerde
  Como um cliente da API
  Eu quero acessar os endpoints de usuários
  Para verificar a funcionalidade básica e as respostas

  Contexto: API está rodando
    Dado que o serviço da API está acessível na url "http://localhost:5000"

  @get_all_usuarios
  Cenário: Buscar a lista de todos os usuários
    Quando eu faço uma requisição GET para "/usuarios"
    Então o status code da resposta deve ser 200
    E o corpo da resposta (JSON) deve ser uma lista
    E o corpo da resposta (JSON) deve corresponder ao schema "usuarios_lista_schema.json"

  @get_root
  Cenário: Verificar a rota raiz da API
    Quando eu faço uma requisição GET para "/"
    Então o status code da resposta deve ser 200


  @not_found
  Cenário: Tentar acessar uma rota inexistente
    Quando eu faço uma requisição GET para "/rota-que-nao-existe"
    Então o status code da resposta deve ser 404
