import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://Vignesh:vtg@servarcluster.mscwh.mongodb.net/servar?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
)
db = client['servar']