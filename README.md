# AniTrack-API
The project consists of a browser extension for users, server-side (this repository), and an instance of Apache Superset. This repository serves as the server, which stores user information, records anime viewing data, and maintains its own anime database that is continuously updated as users watch anime.

This project is designed for conducting detailed analysis of anime viewing. It aims to provide accurate information about the analytics of viewing not only to the users themselves, but also enables content creators to study the analytics of their subscribers.

The project is written in Python + FastAPI. SQLAlchemy is used for database operations. Additionally, an object-oriented approach is employed to implement functionality for interacting with program components through commands (Command class). This ensures flexibility in expanding the server-side and supporting legacy functionality.

Проект включает в себя браузерное расширение для пользователей, **серверную часть (данный репозиторий)** и поднятый инстанс Apache Superset. 
Данный репозиторий представляет собой сервер, который хранит информацию о пользователях, записывает данные о просмотре аниме и содержит собственную базу данных аниме, которая пополняется по мере просмотра аниме пользователями.

Этот проект предназначен для проведения детального анализа просмотра аниме. Он стремится предоставить точную информацию об аналитике просмотра не только самим пользователям, но и дает возможность контент-мейкерам изучать аналитику своих подписчиков.

Проект написан на Python + FastAPI.
Для работы с базой данных: SQLAlchemy.
Также используется объектно-ориентированный подход для реализации функционала работы с компонентами программы через команды (класс Command). Это обеспечивает гибкость в расширении серверной части и поддержке предыдущего функционала.
