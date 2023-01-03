# Ecommerce_Django
Descrição: Site ecommerce usando django

Frameworks: Django e Bootstrap

Linguagens: HTML, CSS, Javascript, Python

Banco de dados: mysql do xampp

# Como usar

Necessário ter o python instalado!!!!

1 - Use o comando <code>git clone 'https://github.com/pabloDPaula/Ecommerce_Django'</code> para copiar este projeto para seu PC

2 - Instale o pycharm e crie um projeto com o nome "ecommerce" e cole tudo dentro da pasta "Ecommerce_Django" para este projeto

3 - Abra o terminal do pycharm e cole estes comandos:

- <code>pip install django</code>
- <code>pip install django-crispy-forms</code>
- <code>pip install pillow</code>
- <code>pip install fontawesomefree</code>
- <code>pip install django_summernote</code>
- <code>pip install mysqlclient</code>

4 - Instale o XAMPP em seu computador e inicie o Apache e o MySQL

5 - Clique em admin do modulo mysql do XAMPP para abrir o phpmyadmin 

6 - Crie um banco de dados com o nome "ecommerce_django" 

- Em loja/settings.py terá um dicionário chamado DATABASES caso queira mudar host, port ou nome do banco de dados

7 - Use os seguintes comandos no terminal do pycharm

- <code>python manage.py makemigrations</code></code></code>
- <code>python manage.py migrate</code></code>

8 - Para executar o projeto use o comando <code>python manage.py runserver</code>

# Admin Django

1 - Abra o terminal do pycharm e execute o comando <code>python manage.py createsuperuser</code> 

- Irá pedir um username, email e password

2 - Para acessar o admin django do nosso projeto basta abrir essa url "http://127.0.0.1:8000/admin" 

