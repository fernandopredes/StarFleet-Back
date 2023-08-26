from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """
    Define como deve ser a estrutura do dado após criação de um novo usuário.
    """
    id = fields.Int(dump_only=True, description="id do usuário")
    name = fields.Str(required=True, description="nome do usuário")
    password = fields.Str(required=True, load_only=True, description="password do usuário")
    email = fields.Email(required=True, description="e-mail do usuário")
    profile_pic = fields.Str(description="URL da imagem de avatar")


    class Meta:
        description = "Define como um novo usuário a ser inserido deve ser representado"

class UserLoginSchema(Schema):
    """
    Define como deve ser a estrutura para realizar o login de um usuário.
    """
    email = fields.Email(required=True, description="e-mail do usuário")
    password = fields.Str(required=True, load_only=True, description="password do usuário")

    class Meta:
        description = "Define como um login de usuário deve ser representado"

class CreateUserSchema(Schema):
    """
    Define como deve ser a estrutura do dado após criação de usuário.
    """
    message = fields.String(description="Mensagem de usuário criado")

    class Meta:
        description = "Esquema de mensagem após a criação de usuário."

class UserTokenSchema(Schema):
    """
    Define como deve ser a estrutura do dado após um login.
    """
    access_token = fields.String(description="Token de acesso")
    user_id = fields.Int(description="Id do usuário")

    class Meta:
        description = "Esquema para resposta da rota de login do usuário"

class PostSchema(Schema):
    """
    Define como o post deve ser apresentado.
    """
    id = fields.Int(dump_only=True, description="Id of the post")
    title = fields.String(validate=validate.Length(max=100), required=True, description="titulo post")
    abstract = fields.String(validate=validate.Length(max=255), required=True, description="resumo do post")
    text = fields.String(validate=validate.Length(max=2200), required=True, description="texto do post")
    image_one = fields.String(required=True, description="primeira imagem post")
    image_two = fields.String(required=True, description="secunda post")
    user_id = fields.Int(required=True, description="Id do usuário que criou o post")


    class Meta:
        description = "Define como o post vai ser apresentado"

class NewPostSchema(Schema):
    """
    Define como o post deve ser criado.
    """

    title = fields.String(validate=validate.Length(max=100), required=True, description="titulo post")
    abstract = fields.String(validate=validate.Length(max=255), required=True, description="resumo do post")
    text = fields.String(validate=validate.Length(max=2200), required=True, description="texto do post")
    image_one = fields.String(required=True, description="primeira imagem post")
    image_two = fields.String(required=True, description="secunda post")
    user_id = fields.Int(required=True, description="Id do usuário que criou o post")


    class Meta:
        description = "Define como o post vai ser apresentado"


class UpdatePostSchema(Schema):
    """
    Define a estrutura do post após o update.
    """
    title = fields.String(validate=validate.Length(max=100), required=False, missing=None, description="titulo post")
    abstract = fields.String(validate=validate.Length(max=255), required=False, missing=None, description="resumo do post")
    text = fields.String(validate=validate.Length(max=2200), required=False, missing=None, description="texto do post")
    image_one = fields.String(required=False, missing=None, description="primeira imagem do post")
    image_two = fields.String(required=False, missing=None, description="segunda imagem do post")
    date = fields.Date(required=False, missing=None, description="data de criação do post")

    class Meta:
        description = "Define como o post vai aparecer depois do update"


class DeletePostSchema(Schema):
    """
    Define a estrutura depois de delatar o post.
    """
    message = fields.String(description="Status da opeção")
    id = fields.Int(description="Id do post deletado")

    class Meta:
        description = "Schema da rota de delete do post"
