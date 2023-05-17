from superset.database import engine

DEFAULT_ROLE_ID = 8  # It's Common User role


def create_user_in_superset(username, hashed_password, email, first_name, last_name, created_on, active):
    with engine.connect() as con:
        user_id = con.execute(
            """
            SELECT MAX(id) from ab_user;
            """
        ).all()[0][0] + 1

        ab_user_role_record_id = con.execute(
            """
            SELECT MAX(id) from ab_user_role;
            """
        ).all()[0][0] + 1

        con.execute(
            f"""
            INSERT INTO ab_user (id, first_name, last_name, username, password, active, email, created_on) VALUES (
                {user_id}, '{first_name}', '{last_name}', '{username}', '{hashed_password}', '{active}', '{email}', '{created_on}'
            ) 
            """
        )

        con.execute(
            f"""
            INSERT INTO ab_user_role (id, user_id, role_id) VALUES (
                {ab_user_role_record_id}, {user_id}, {DEFAULT_ROLE_ID}
            )
            """
        )


def get_user_from_superset(username: str):
    with engine.connect() as con:
        return con.execute(
            f"""
            SELECT * from ab_user WHERE username='{username}';
            """
        ).all()
