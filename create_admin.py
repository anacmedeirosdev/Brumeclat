from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

def criar_administrador():
    app = create_app()
    
    with app.app_context():
        nome_admin = "Administrador Bruméclat"
        telefone_admin = "84911111111" 
        senha_admin = "admin123"         
        
        usuario_existente = Usuario.query.filter_by(telefone=telefone_admin).first()
        
        if usuario_existente:
            print(f"Erro: O telefone {telefone_admin} já está cadastrado no sistema!")
            return

        # Gera o hash da senha exatamente como no seu auth.py
        senha_criptografada = generate_password_hash(senha_admin)
        
        # Cria a instância do usuário mudando explicitamente o tipo para 'admin'
        novo_admin = Usuario(
            nome=nome_admin,
            telefone=telefone_admin,
            senha=senha_criptografada,
            tipo='admin' 
        )
        
        try:
            db.session.add(novo_admin)
            db.session.commit()
            print("==================================================")
            print(" Administrador criado com sucesso!")
            print(f" Nome:     {nome_admin}")
            print(f" Telefone: {telefone_admin}")
            print(f" Senha:    {senha_admin} (Salva como hash no banco)")
            print("==================================================")
        except Exception as e:
            db.session.rollback()
            print(f"Ocorreu um erro ao salvar no banco de dados: {e}")

if __name__ == '__main__':
    criar_administrador()