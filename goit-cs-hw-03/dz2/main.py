from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://goitlearn:j345nv3l3k5v3l%3B@cluster0.k8awq13.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book

result_many = db.cats.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
        {
            "name": "Markiz",
            "age": 1,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
        {
            "name": "Jek",
            "age": 12,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)
#print(result_many.inserted_ids)
    
    
def get_all():
    result = db.cats.find({})
    for el in result:
        print(el)

def get_catinfo(name):
    result = db.cats.find_one({"name": name})
    print(result)
    
def update_catinfo_age(name, age):
    db.cats.update_one({"name": name}, {"$set": {"age": age}})
    result = db.cats.find_one({"name": name})
    print(result)
    
def update_catinfo_feuture(name, feature):
    db.cats.update_one({"name": name}, {"$push": {"features": feature}})
    result = db.cats.find_one({"name": name})
    print(result)
    
    
def delete_cat(name):
    db.cats.delete_one({"name": name})
    result = db.cats.find_one({"name": name})
    print(result)
    
def delete_all():
    db.cats.delete_many({})
    result = result = db.cats.find({})
    print(result)
    
        
get_all()
get_catinfo("Markiz")
update_catinfo_age("Markiz", 15)
update_catinfo_feuture("Markiz", "Любить гратися")
delete_cat("Markiz")
delete_all()

