# Домашнее задание к лекции «Asyncio»

Написан на asyncio + aiopg скрипт.
Скрипт выгружает людей из sqlite [базы](contacts.db), и отправляет им email с заданным шаблоном:

```
Уважаемый <Имя пользователя>! 
Спасибо, что пользуетесь нашим сервисом объявлений.
``` 
