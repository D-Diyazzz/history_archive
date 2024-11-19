from sqlalchemy import text

# Запрос для вставки нового пользователя
insert_user = text("""
    insert into "user"(
        "id",
        "firstname",
        "lastname",
        "email",
        "role",
        "hashed_password",
        "created_at"
    ) values (
        :id,
        :firstname,
        :lastname,
        :email,
        :role,
        :hashed_password,
        :created_at
    ) returning id
""")

# Запрос для выборки всех пользователей
select_users = text("""
    select 
        id,
        firstname,
        lastname,
        email,
        role,
        hashed_password,
        created_at
    from "user"
""")

# Запрос для выборки пользователя по id
select_user_by_id = text("""
    select 
        id,
        firstname,
        lastname,
        email,
        role,
        hashed_password,
        created_at
    from "user"
    where id = :id
""")

select_user_by_email = text("""
    select * from "user" where email=:email
""")

# Запрос для обновления данных пользователя
update_user = text("""
    update "user"
    set 
        firstname = :firstname,
        lastname = :lastname,
        email = :email,
        role = :role,
        hashed_password = :hashed_password
    where id = :id
""")

# Запрос для удаления пользователя по id
delete_user = text("""
    delete from "user"
    where id = :id
""")

