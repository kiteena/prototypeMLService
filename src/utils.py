
def makeDictionary(data):
    columns = ["user", "item", "rating", "est"]
    return [dict(zip(columns, l)) for l in data]