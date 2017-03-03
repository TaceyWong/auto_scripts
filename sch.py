from plan import Plan

cron = Plan()

cron.command('python auto_weibo_api.py', every='1.day', at='12:00')

if __name__ == "__main__":
    cron.run()
