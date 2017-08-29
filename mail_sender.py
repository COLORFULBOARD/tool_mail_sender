# -*- coding: utf-8 -*-
import threading
import smtplib
from email.mime.text import MIMEText


class MailSender(object):
    """smtplibの軽いWrapperクラス"""

    def __init__(self, user, password, smtp, port, sender=None, tls=True):
        """イニシャライザ

        :param user: 認証が必要な場合のユーザーID
        :param password: 認証が必要な場合のパスワード
        :param smtp: 送信に利用するSMTPサーバー
        :param port: 送信に利用するポート
        :param sender: 送信元メールアドレス。指定しなければ認証時のユーザーIDになる
        :param tls: TLSを利用しない場合False
        """
        self.user = user
        self.password = password
        self.sender = sender if sender else user
        self.smtp = smtp
        self.port = port
        self.tls = tls

    def send(self, msg, title=None, to=None, async=True):
        """メールを送信する

        :param msg: メール本文
        :param title: メールのタイトル
        :param to: 宛先。文字列or文字列のリストor文字列のタプル
        :param async: threadingを利用しない場合はFalse
        """
        if async:
            sender = threading.Thread(target=self._send, args=(msg, title, to))
            sender.start()
        else:
            self._send(msg, title, to)

    def _send(self, msg, title=None, to=None):
        message = MIMEText(msg)
        message['Subject'] = title if title else ''
        message['From'] = self.sender if self.sender else self.user
        if isinstance(to, str):
            to = (to,)
        elif not isinstance(to, (list, tuple)):
            to = ['']
        message['To'] = ', '.join(to)
        with smtplib.SMTP(self.smtp, self.port) as server:
            if self.tls:
                server.starttls()
                server.ehlo()
            if self.user and self.password:
                server.login(self.user, self.password)
            server.send_message(message)

