import sys

import os
import psycopg2
import urlparse

con = None
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS 'FuturesContractsCreated'")
cur.execute("CREATE TABLE 'FuturesContractsCreated'(id  serial, blockchainderivativesid TEXT, buyerethereumaddress TEXT, sellerethereumaddress TEXT, deliverydate TEXT, numberofunits TEXT, commodityname TEXT, price INT, margin INT, soliditycodeinitial TEXT)")

con.commit()
con.close()