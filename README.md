# manager

Запустить docker-compose

Пользователь может регистрироваться /api/register/

Авторизоваться /api/token/

Смотреть информацию профиля /api/profile/ 

Просматривать/изменять/добавлять/удалять категории /api/profile/category/  /api/profile/category/<<id>>/
  
Осуществлять/просматривать транзакции /api/profile/transaction/   (action=debit - списание, 
                                                                   action=replenish - пополнение)
  
Сортировать транзакции по value  /api/profile/transaction/filter_transaction?ordering=value
