# -*- coding: utf-8 -*-

import sqlite3

class BooksPipeline(object):
    def process_item(self, item, spider):
        self.conn.execute('insert into books (categoria, titulo, id, preco_sem_taxa, preco_real, taxa, estoque, reviews, estrelas) values (:categoria, :titulo, :id, :preco_sem_taxa, :preco_real, :taxa, :estoque, :reviews, :estrelas)',
                            item)
        self.conn.commit()
        return item

    def create_table(self):
        result = self.conn.execute('SELECT name FROM sqlite_master WHERE type="table" AND name = "books"')

        try:
            _ = next(result)
        except StopIteration as _:
            self.conn.execute('create table books (categoria varchar(150), titulo varchar(150), id varchar(150), preco_sem_taxa varchar(150), preco_real varchar(150), taxa varchar(150), estoque varchar(150), reviews varchar(150), estrelas varchar(150))')

    def open_spider(self, spider):
        self.conn = sqlite3.connect('/home/matheus/Documentos/books-scrap/data/db_books.sqlite3')
        self.create_table()
    
    def close_spider(self, spider):
        self.conn.close()