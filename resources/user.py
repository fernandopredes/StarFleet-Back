from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, jwt_required, get_jwt_identity
from cloudinary.uploader import upload


from db import db
from models import UserModel
from schemas import UserSchema, UserLoginSchema, UserTokenSchema, CreateUserSchema

blp = Blueprint("Users", __name__, description="Operações de vizualização, adição e login com Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,CreateUserSchema, description="Sucesso. Retorna uma mensagem confirmando que o usuário foi criado.")
    def post(self, user_data):
        """ Rota para registrar um usuário.

        Retorna uma mensagem confirmando que o usuário foi criado.

        """
        if UserModel.query.filter(UserModel.name == user_data["name"]).first():
            abort(409, message="Já existe um usuário com esse nome.")

        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="Já existe um usuário com esse e-mail.")

        user = UserModel(
            name = user_data["name"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"]),

        )
        db.session.add(user)
        db.session.commit()

        return {"message": "Usuário criado."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(200, UserTokenSchema, description="Sucesso. Retornado token de acesso e o id do usuário.")
    def post(self, user_data):
        """ Rota para realizar o login de um usuário.

        Retorna o id do usuário e gera um token de acesso.

        """
        user = UserModel.query.filter(
            UserModel.email == user_data['email']
        ).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token, "user_id": user.id}

        abort(401, message="Invalid cedentials.")

@blp.route("/users")
class UsersList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True), description="Sucesso. Retorna uma lista de todos os usuários.")
    def get(self):
        """ Rota para buscar todos os usuários.

        Retorna uma lista de todos os usuários.
        """
        users = UserModel.query.all()
        return users

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema, description="Sucesso. Retorna as informações recebidas do usuário referente ao id escolhido.")
    def get(self, user_id):
        """ Rota para pegar um único usuário pelo id.

        Retorna uma representação das informações de um usuário.

        """
        user = UserModel.query.get_or_404(user_id)
        return user

@blp.route('/upload_pic', methods=['POST'])
class UserPicUpload(MethodView):
    @jwt_required()
    @blp.response(200, description="Sucesso. Retorna uma mensagem confirmando que a foto do perfil foi carregada.")
    def post(self):
        """ Rota para carregar a foto do perfil do usuário.

        Retorna uma mensagem confirmando que a foto do perfil foi carregada.

        """
        # Get the current user
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get(current_user_id)

        if 'file' not in request.files:
            abort(400, message="Nenhum arquivo carregado.")
        file = request.files['file']

        if file.filename == '':
            abort(400, message="Nenhum arquivo detectado.")

        try:
            res = upload(file)
            image_url = res['secure_url']
            current_user.profile_pic = image_url  # save URL to profile_pic column
            db.session.commit()  # commit changes to database
            return {"message": "Profile picture uploaded successfully."}
        except Exception as e:
            abort(500, message=str(e))
