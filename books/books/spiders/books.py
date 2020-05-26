# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    #allowed_domains = ['books.toscrape.com/index.html']
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']

    def start_requests(self):
        """
        Funcao para iniciar os requestes nos URLs

        Retorna uma URL.
        """
        pages = 50

        for i in range(1, pages + 1):
            url = 'http://books.toscrape.com/catalogue/page-%s.html' % i
            print(url)
            yield scrapy.Request(url,
                                 callback=self.parse)

    def parse(self, response):
        """
        Funcao responsavel por retornar todos os livros da pagina
        """
        list_books = response.xpath('//div[@class="image_container"]/a/@href').extract()
        for url in list_books:
            start_url = 'http://books.toscrape.com/catalogue/'
            url_book = start_url + url
            yield scrapy.Request(url_book,
                                callback=self.parse_detail)

    def parse_detail(self, response):
        """
        Funcao responsavel extrair as informacoes dentro da pagina do livro em questao
        """
        titulo = response.xpath('//*[@id="default"]/div/div/ul/li[4]/text()').extract_first()
        categoria = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').extract_first()
        tabela_conteudo = response.xpath('//td/text()').extract()
        estrelas = response.xpath('//p[contains(@class, "star-rating")]/@class').extract_first()  

        yield {
            'categoria': categoria,
            'titulo': titulo,
            'id': tabela_conteudo[0],
            'preco_sem_taxa': tabela_conteudo[2],
            'preco_real': tabela_conteudo[3],
            'taxa': tabela_conteudo[4],
            'estoque': tabela_conteudo[5],
            'reviews': tabela_conteudo[6],
            'estrelas': estrelas,
        }
