from environs import Env
env = Env()
env.read_env()
# BOT_TOKEN=env.str('BOT_TOKEN')
ADMINS=env.list('ADMINS')
# BOT_ID=env.str('BOT_ID')

BOT_TOKEN = '7888745554:AAFF-AGCb6KGNGCNVSJW78DoSBeF_wyzTwk'
BOT_ID = 7888745554