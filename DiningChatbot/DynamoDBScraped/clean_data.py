import json

def main():
    """Clean scraped Yelp businesses.
       Create 2 json files:
        - business_dynamo.json: cleaned businesses info for DynamoDB
        - business_es.json: businesses info for ElasticSearch, only store restaurnat ID and Cuisine type
    """
    json_file = '../data/businesses_raw.json'
    businesses_raw = json.load(open(json_file, "r"))

    # keep only required fields:
    # Requirements: Business ID, Name, Address, Coordinates, Number of Reviews, Rating, Zip Code
    businesses_dynamo = list()
    businesses_es = list()
    for cuisine in businesses_raw:
        for buz in businesses_raw[cuisine]:
            # format address
            if not buz['location']['address1']:
                # no address info, skip this business
                continue
            addr = buz['location']['address1']
            if buz['location']['address2'] and len(buz['location']['address2'])!=0:
                addr += ' ' + buz['location']['address2']
            if buz['location']['address3'] and len(buz['location']['address3'])!=0:
                addr += ' ' + buz['location']['address3']
            addr += ', ' + buz['location']['city']
            # get cleaned business info
            cleaned = dict(
                id = buz['id'],
                name = buz['name'],
                category = cuisine,
                address = addr,
                coordinates = buz['coordinates'],
                review_count = buz['review_count'],
                rating = buz['rating'],
                zip_code = buz['location']['zip_code']
            )
            # check for None type or empty strings
            invalid = 0
            for item in cleaned:
                if not cleaned[item]:
                    invalid = 1
                elif isinstance(cleaned[item], str) and len(cleaned[item]) == 0:
                    invalid = 1
            if invalid == 1:
                continue
            # add to businesses_dynamo
            businesses_dynamo.append(cleaned)
            # add to businesses_es
            es_doc = dict(
                type = 'Restaurant',
                restaurant_id = cleaned['id'],
                cuisine = cleaned['category']
            )
            businesses_es.append(es_doc)
    print("Total number of restaurants is {}. ".format(len(businesses_dynamo)))

    # save results
    dynamo_file = '../data/businesses_dynamo.json'
    es_file = '../data/businesses_es.json'
    json.dump(businesses_dynamo, open(dynamo_file, "w"))
    json.dump(businesses_es, open(es_file, "w"))


if __name__ == '__main__':
    main()