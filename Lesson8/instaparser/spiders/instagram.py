# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'onliskill_udm'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1591291623:AeZQANjUYQQHAtsDlsZWqwjk1fmzZlqXoSBP77giDsKyGd0hzUC4A4SGhA7u91hdjOsVYP2orQiwNlNRBlOQRwVVUZRsQXgrmcOf3r38LIIljjOGk4Cq8yO7B7sdzHVPOMgJSkKNbFBGWZmv'
    inst_login_link = 'https://instagram.com/accounts/login/ajax/'
    parser_user = 'staud.clothing'

    hash_posts = '7c8a1055f69ff97dc201e752cf6f0093'
    hash_post = '552bb33f4e58c7805d13d4f95da7d3a1'
    graphql_url = 'https://www.instagram.com/graphql/query/?'


    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
                self.inst_login_link,
                method = 'POST',
                callback = self.parse_user,
                formdata={'username':self.insta_login,
                          'enc_password':self.insta_pass},
                headers={'X-CSRFToken':csrf_token}
        )

        pass

    def parse_user(self, response):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parser_user}',
                callback = self.user_data_parse,
            )




    def user_data_parse(self, response):
        user_id = self.fetch_user_id(response.text, self.parser_user)
        variables = {"id": user_id,
                     "first":50
        }

        url_posts = f'{self.graphql_url}query_hash={self.hash_posts}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback = self.posts_parse,
            cb_kwargs= {'user_id':user_id,
                        'variables': deepcopy(variables)}
        )


    def posts_parse(self,response,user_id, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']

            url_posts = f'{self.graphql_url}query_hash={self.hash_posts}&{urlencode(variables)}'

            yield response.follow(
                url_posts,
                callback=self.posts_parse,
                cb_kwargs={'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        posts = j_body.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstaparserItem(
                user_id = user_id,
                photo = post['node']['display_url'],
                likes = post['node']['edge_media_preview_like']['count'],
                post_data = post['node']
            )

            yield item



    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')