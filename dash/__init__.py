from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(views.secon_views.secon, 'interval', seconds=3, id='test', replace_existing=True)
    scheduler.start()