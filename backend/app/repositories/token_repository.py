from models.token import TokensDB

class TokenRepository:
    def __init__(self, session):
        self.session = session

    def create_token(self, token: TokensDB):
        self.session.add(token)
        self.session.commit()

    def get_tokens(self):
        return self.session.query(TokensDB).all()

    def get_token(self, token: str):
        return self.session.query(TokensDB).filter(TokensDB.token == token).first()

    def delete_token(self, token: str):
        token = self.get_token(token)
        self.session.delete(token)
        self.session.commit()