def switch_user(user_name: str) -> None:
    import pwd
    import os

    print(f"Switching to user: {user_name}")
    user = pwd.getpwnam(user_name)

    os.setgid(user.pw_uid)
    os.setuid(user.pw_uid)
