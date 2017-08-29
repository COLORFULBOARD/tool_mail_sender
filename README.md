# What is this?
Pythonで簡単にメールを送るためのsmtplibの簡単なラッパーです。  
threadingで非同期処理しています。

# How to use

Gmailであればこんな感じで動きます。
ただし、2段階認証有効にしていると認証で弾かれます。

```python
from mail_sender import MailSender

mail_sender = MailSender(
    user='XXX@gmail.com',
    password='XXX@gmail.comのパスワード',
    smtp='smtp.gmail.com',
    port=587
)
mail_sender.send(
    msg='本文',
    title='タイトル',
    to='宛先メールアドレス'
)
```
