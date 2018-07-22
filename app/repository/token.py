"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""
from datetime import datetime, timedelta

from app.model.token import TokenModel


class TokenRepository:
    def save(self, data, session):
        try:
            print("En token repository save")
            print(data)
            last_token = session.query(TokenModel).filter(TokenModel.user_id == data['user_id']).delete()
            token = TokenModel()
            token.user_id = data['user_id']
            token.access_token = data['access_token']
            token.refresh_token = data['refresh_token']
            token.issued_at = data['issued_at']
            token.access_token_expires_at = data['access_token_expires_at']
            token.refresh_token_expires_in = data['refresh_token_expires_in']

            session.add(token)
            session.commit()
            return token
        except Exception as exc:
            msg = "TokenRepository.error::{}".format(exc)
            print(exc)
            session.rollback()

    def exist_refresh(self, refresh_token, session):
        try:
            actual_token = session.query(TokenModel).filter(TokenModel.refresh_token == refresh_token).first()
            print(refresh_token)
            print(actual_token)
            return actual_token
        except Exception as exc:
            print("TokenRepository.get_by_refresh.error::{}".format(exc))
            return None
