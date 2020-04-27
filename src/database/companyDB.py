from bson.objectid import ObjectId


class CompanyDB(object):

    def __init__(self, mongo):
        # API Database
        self.db = mongo["reborn2020"]
        self.collection = self.db["companies"]

    def get_company_by_id(self, company_id):
        myquery = {"_id": ObjectId(company_id)}

        found_company = self.collection.find_one(myquery)
        return found_company

    def get_all_markers(self):
        # database = self.collection.find()
        # markerList = []
        # for x in database:
        #     markerList.append((x["coords"], x["_id"]))
        # print(markerList)
        return [[x["coords"], x["_id"], x["type"]] for x in self.collection.find() if "coords" in x and x["coords"]]

    def find_company(self, query):
        myquery = {"$or":[ {"$text": {"$search": query}}, {"jobs": query}]}

        result = self.collection.find(myquery)
        return [{key: val for key, val in item.items() if key not in ["email", "phone", "coords"]} for item in result]

    # Read Record
    # def read(self, name, arg=False):
    #
    #     if arg:
    #
    #         return self.api[name].find_one(arg['query'])
    #
    #     else:
    #
    #         items = []
    #
    #         for item in self.api[name].find():
    #             item.pop('_id')
    #
    #             items.append(item)
    #
    #         return items

    # Create Record
    def create(self, company):
        self.collection.insert_one(company)
        return self.collection.find_one({'name': company.get('name')})
        #
        # if arg:
        #
        #     co = self.api[name]
        #
        #     id = arg['id'] = co.count() + 1
        #
        #     if co.insert_one(arg):
        #         return co.find_one({'id': id})

    # Update
    # def update(self, name, arg):
    #
    #     co = self.api[name]
    #
    #     if co.update_one(arg['query'], {'$set': arg['data']}).matched_count > 0:
    #         return co.find_one(arg['query'])
    #
    # # Delete
    # def delete(self, name, arg=False):
    #
    #     co = self.api[name]
    #
    #     if not co.delete_one(arg['query']):
    #         return
