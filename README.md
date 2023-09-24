# StarFleet - Back

Este backend foi desenvolvido como parte do MVP 3 da pós-graduação da PUC-Rio. A aplicação foi criada pensando nos fãs de Star Trek, fornecendo uma plataforma onde os usuários podem se autenticar, postar conteúdos, participar de quizzes e ver novos conteúdos.

## 🚀 Recursos

### Usuários
- Registro de usuários com foto de perfil.
- Autenticação e autorização.
- Integração com a API Cloudinary para armazenamento de imagens.

### Quizzes
- Obtenção de quizzes para testar usuários.

### Posts
- CRUD completo de posts.

## 💻 Tecnologias Utilizadas

- Python
- Flask
- Cloudinary


## 🐳 Executando o Projeto com Docker

```bash
# Construir a imagem
docker build -t nome-da-imagem .

# Rodar o contêiner
docker run -p 5000:5000 nome-da-imagem
```

## 📦 Integração com Cloudinary

A integração com o Cloudinary é realizada através da API, permitindo o armazenamento de imagens. Ao registrar ou atualizar informações de perfil, os usuários podem fazer upload de imagens, que são enviadas diretamente para o Cloudinary. O Cloudinary, por sua vez, retorna uma URL única para cada imagem, que é armazenada em nosso banco de dados.

Para configurar a integração em um ambiente de desenvolvimento você deve retirar o final ".example" do arquivo .env e fornecer as credenciais do Cloudinary, que incluem um `CLOUD_NAME`, `API_KEY` e `API_SECRET`. Estas são configuradas como variáveis de ambiente e são usadas pela aplicação Flask para autenticar e interagir com o serviço Cloudinary.
