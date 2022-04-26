from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
# IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
WORDS_PASS  = ['a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', '1', '2', '3', '4', '5', '6', '7', '8', '9']
user_bot_id = env.int("user_bot_id")