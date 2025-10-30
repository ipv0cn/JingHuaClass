from JingHua import User
import config


if __name__ == "__main__":
    user = User()
    user.login(config.USERNAME, config.PASSWORD)
