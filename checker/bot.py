#bot
import aiogram
import api
import db_adapter as db
import datetime

db_ = db.db_usage(db.DbConnection())
print (db_.decode('Шерем'))


ap = api.api_request('MOW','LED', (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d'))

print (ap.cheapest_ticket_in_date().json())


