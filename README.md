# Website_for_recruiters

Instructions for installing and launching the project:

+ Copy repository address: https://github.com/DaryaKhatsuk/Website_for_recruiters.git

+ Launch Terminal with Command Prompt(cmd)

+ Clone the project with: git clone https://github.com/DaryaKhatsuk/Website_for_recruiters.git

+ Use **pip install -r requirements.txt** to load imports from requirements.txt

+ In the **settings.py** file, include the actual **DATABASES**
+ In the terminal, run and check in the migrations with:

      python manage.py makemigrations
    
      python manage.py migrate
    
+ Create a superuser with the command: **python manage.py createsuperuser**
+ Start the server with a terminal command: **python manage.py runserver**
