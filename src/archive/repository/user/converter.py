from src.archive.domains.user import User, Role


def user_to_dict(model: User):

    model_dict = {
        "id": model.get_id,
        "firstname": model.get_firstname,
        "lastname": model.get_lastname,
        "email": model.get_email,
        "hashed_password": model.get_password,
        "role": model.get_role,
        "created_at": model.get_created_at
    }

    return {k: v for k, v in model_dict.items() if v is not None}


def dict_to_user(user):

    return User.upload(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=user.hashed_password,
        role=user.role,
        created_at=user.created_at
    )
