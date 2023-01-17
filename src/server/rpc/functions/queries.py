# List all stores and numbers
def list_stores():
    return """SELECT unnest(xpath('/Dataset/Store/Store_name/text()', xml))::text as store_name,
        unnest(xpath('/Dataset/Store//@number', xml))::text as store_number
FROM imported_documents
WHERE is_deleted = false
ORDER BY store_number;"""


# List all the countries store numbers
def list_countries_stores():
    return """SELECT (unnest(xpath('/Dataset/Cities/City[@id=' || city_ref || ']/Name/text()', xml)))::text as city_name,
       count(*) as number_stores
FROM (SELECT xml,
             unnest(xpath('/Dataset/Store/Address/City/@ref', xml)) ::text::int as city_ref
      FROM imported_documents
      WHERE is_deleted = false
      ORDER BY city_ref
) as result
group by city_name;"""


# List number of stores by ownership type
def list_ownership_stores():
    return """SELECT unnest(xpath('/Dataset/Store/Ownership_type/text()', xml))::text as ownership_type,
       count(*) as number_stores
FROM imported_documents
WHERE is_deleted = false
GROUP BY ownership_type;"""


# List all portuguese stores and the number of stores in each city
def list_portuguese_cities_stores():
    return """SELECT city_name,
       count(*) as number_stores
FROM (SELECT xml,
             unnest(xpath('/Dataset/Cities/City[Country = "PT"]/Name/text()', xml))::text as city_name
      FROM imported_documents
      WHERE is_deleted = false
) as result
GROUP BY city_name
ORDER BY city_name;"""


# List all the stores with contact information
def list_stores_contacts():
    return """SELECT unnest(xpath('/Dataset/Store/Store_name/text()', xml))::text as store_name,
       unnest(xpath('/Dataset/Store/Phone_number/text()', xml))::text as phone_number
FROM imported_documents
WHERE is_deleted = false;"""


# List all the stores that exist in the city referenced
def list_stores_cities(city):
    return f"""SELECT (unnest(xpath('/Dataset/Store[Address/City/@ref=' || city_id || ']/Store_name/text()', xml)))::text as city_name
FROM (SELECT xml,
             unnest(xpath('/Dataset/Cities/City[Name = "{city}"]/@id', xml)) ::text::int as city_id
      FROM imported_documents
      WHERE is_deleted = false
      ORDER BY city_id
) as result;"""
