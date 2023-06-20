import sqlalchemy
from sqlalchemy.orm import sessionmaker
from homework_orm import create_tables, Publisher, Book, Shop, Sale, Stock
from pprint import pprint

login = 'postgres'
password = 'lastochka86'
table_name = 'orm_base'

DSN = f'postgresql://{login}:{password}@localhost:5432/{table_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

import json
with open('tests_data.json') as file:
    data = json.load(file)
    publisher_name = [i['fields'] for i in data if i['model'] == 'publisher']
    title_id = [i['fields'] for i in data if i['model'] == 'book']
    shop_name = [i['fields'] for i in data if i['model'] == 'shop']
    stock_id = [i['fields']for i in data if i['model'] == 'stock']
    sale_data = [i['fields']for i in data if i['model'] == 'sale']

for pub in publisher_name:
    publisher = Publisher(name = pub['name'])
    session.add(publisher)
for b_t in title_id:
    title = b_t['title']
    id_publisher = b_t['id_publisher']
    session.query(Publisher).filter_by(id=id_publisher).one()
    book = Book(title = title, id_publisher = id_publisher)
    session.add(book)
for shop in shop_name:
    name = Shop(name = shop['name'])
    session.add(name)
for data in stock_id:
    id_shop = data['id_shop']
    id_book = data['id_book']
    count = data['count']
    session.query(Book).filter_by(id=id_book).one()
    session.query(Shop).filter_by(id=id_shop).one()
    stock = Stock(id_shop = id_shop, id_book = id_book, count = count)
    session.add(stock)
for sales in sale_data:
    prices = sales['price']
    sale_date = sales['date_sale']
    id_stock = sales['id_stock']
    sale_count = sales['count']
    session.query(Stock).filter_by(id=id_stock).one()
    sale = Sale(price = prices, date_sale = sale_date, id_stock = id_stock, count = sale_count)
    session.add(sale)
session.commit()
session.close()

name_or_id = input()
if name_or_id.isdigit():
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock)\
        .join(Book).join(Shop).join(Publisher).filter(Publisher.id == name_or_id).all()
    for item in q:
        print(f'{item[0]} | {item[1]} | {item[2]} | {item[3]}')
else:
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock) \
        .join(Book).join(Shop).join(Publisher).filter(Publisher.name == name_or_id).all()
    for item in q:
        print(f'{item[0]} | {item[1]} | {item[2]} | {item[3]}')