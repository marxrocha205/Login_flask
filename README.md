# Sistema de Login e Administração com Flask

Este projeto é um sistema de login e registro simples desenvolvido em Flask que permite a criação de usuários e administradores, gerenciamento de usuários e a criptografia dos dados de usuários em um arquivo JSON. Somente administradores podem criar outros administradores e gerenciar os usuários.

## Funcionalidades

- **Registro de Usuários**: Os usuários podem se registrar com um nome de usuário e senha.
- **Login de Usuários**: Usuários podem fazer login com seu nome de usuário e senha.
- **Criação de Administradores**: Apenas um administrador pode criar outro administrador.
- **Gerenciamento de Usuários**: Administradores podem visualizar, remover e editar usuários.
- **Criptografia de Dados**: Todas as informações de usuários são armazenadas em um arquivo JSON criptografado.
- **Exibição de Usuários**: A lista de usuários é descriptografada e exibida na interface de administração.

## Requisitos

- Python 3.7+
- Flask
- Werkzeug (para hashing de senhas)
- cryptography (para criptografia e descriptografia de dados)