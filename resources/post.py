from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from cloudinary.uploader import upload
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import PostModel
from models import UserModel
from schemas import PostSchema, UpdatePostSchema, DeletePostSchema, NewPostSchema

blp = Blueprint("Posts", __name__, description="Operações com Posts")

@blp.route('/posts')
class PostList(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema(many=True), description="Success. Returns the list of all posts.")
    def get(self):
        """Pega todos os posts"""
        posts = PostModel.query.order_by(PostModel.date.desc()).all()
        post_schema = PostSchema(many=True)
        result = post_schema.dump(posts)

        for post in result:
            user = UserModel.query.get(post['user_id'])
            post['username'] = user.name
            post['profile_pic'] = user.profile_pic

        return result

@blp.route('/create_post', methods=['POST'])
class PostCreation(MethodView):
    @jwt_required()
    @blp.arguments(NewPostSchema, location="json")
    @blp.response(200, description="Success. Returns a message confirming the post has been created.")
    def post(self, args):
        """ Rota para criar um post.

        Retorna uma mensagem confirmando que o post foi criado.

        """
        # pega o usuário atual
        current_user_id = get_jwt_identity()

        # Get the fields from request
        title = args['title']
        abstract = args['abstract']
        text = args['text']

        # Validate the text fields. Return error if not valid.
        if not title or not abstract or not text:
            abort(400, message="Invalid input. Please provide all required fields.")

        try:
            # Cria um novo post com as imagens
            new_post = PostModel(
                user_id=current_user_id,
                title=title,
                abstract=abstract,
                text=text,
            )

            db.session.add(new_post)
            db.session.commit()  # commit mudanças no database

            return {"message": "Post created successfully."}

        except Exception as e:
            abort(500, message=str(e))


@blp.route('/posts/<int:post_id>')
class Post(MethodView):
    @jwt_required()
    @blp.response(200, PostSchema, description="Success. Returns the post with the given id.")
    def get(self, post_id):
        """Pega um único post"""
        post = PostModel.query.get_or_404(post_id)
        return post

    @jwt_required()
    @blp.arguments(UpdatePostSchema, location="json")
    @blp.response(200, PostSchema, description="Success. Returns the updated post.")
    def put(self, parsed_args, post_id):
        """Update de um post"""
        post = PostModel.query.get_or_404(post_id)

        # pega o usuário atual
        current_user_id = get_jwt_identity()

        # verifica se o usuário é o criador do post
        if post.user_id != current_user_id:
            abort(403, message="You do not have permission to edit this post.")

        # atribui os novos valores
        if parsed_args.get('title'):
            post.title = parsed_args['title']
        if parsed_args.get('abstract'):
            post.abstract = parsed_args['abstract']
        if parsed_args.get('text'):
            post.text = parsed_args['text']

        try:
            db.session.commit()  # commita no db
            return PostSchema().dump(post)

        except Exception as e:
            abort(500, message=str(e))

    @jwt_required()
    @blp.response(200, DeletePostSchema, description="Success. Returns a success message and the deleted post.")
    @blp.response(404, description="The id was not found.")
    def delete(self, post_id):
        """Deleta um post"""
        post = PostModel.query.get_or_404(post_id)
        # Pega o usuário atual
        current_user_id = get_jwt_identity()

        # Verifica se o usuário atual é o criador do post
        if post.user_id != current_user_id:
            abort(403, message="You do not have permission to delete this post.")
        db.session.delete(post)
        db.session.commit()
        return {"message":"Post deleted"}, 200
