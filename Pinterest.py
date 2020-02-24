import json
import os

import requests
import mimetypes
import requests.cookies
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
from BookmarkManager import BookmarkManager
from Registry import Registry
from RequestBuilder import RequestBuilder
from requests.structures import CaseInsensitiveDict

AGENT_STRING = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) " \
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

# Pinterest endpoints
HOME_PAGE = 'https://www.pinterest.com/'
LOGIN_PAGE = 'https://www.pinterest.com/login/?referrer=home_page'
CREATE_USER_SESSION = 'https://www.pinterest.com/resource/UserSessionResource/create/'
USER_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserResource/get'
BOARD_PICKER_RESOURCE = 'https://www.pinterest.com/resource/BoardPickerBoardsResource/get'
BOARDS_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardsResource/get'
CREATE_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardResource/create/'
FOLLOW_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardFollowResource/create/'
UNFOLLOW_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardFollowResource/delete/'
FOLLOW_USER_RESOURCE = 'https://www.pinterest.com/resource/UserFollowResource/create/'
UNFOLLOW_USER_RESOURCE = 'https://www.pinterest.com/resource/UserFollowResource/delete/'
USER_FOLLOWING_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserFollowingResource/get'
USER_FOLLOWERS_RESOURCE = 'https://www.pinterest.com/resource/UserFollowersResource/get'
PIN_RESOURCE_CREATE = 'https://www.pinterest.com/resource/PinResource/create/'
REPIN_RESOURCE_CREATE = 'https://www.pinterest.com/resource/RepinResource/create/'
PIN_LIKE_RESOURCE = 'https://www.pinterest.com/resource/PinLikeResource/create/'
PIN_UNLIKE_RESOURCE = 'https://www.pinterest.com/resource/PinLikeResource/delete/'
DELETE_PIN_RESOURCE = 'https://www.pinterest.com/resource/PinResource/delete/'
PIN_COMMENT_RESOURCE = 'https://www.pinterest.com/resource/PinCommentResource/create/'
BOARD_INVITE_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardInviteResource/create/'
BOARD_DELETE_INVITE_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardCollaboratorResource/delete/'
SEARCH_RESOURCE = 'https://www.pinterest.com/resource/SearchResource/get'
BOARD_RECOMMEND_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardContentRecommendationResource/get'
PINNABLE_IMAGES_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/FindPinImagesResource/get'
BOARD_FEED_RESOURCE = 'https://www.pinterest.com/resource/BoardFeedResource/get'
USER_HOME_FEED_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserHomefeedResource/get'
BASE_SEARCH_RESOURCE = 'https://www.pinterest.com/resource/BaseSearchResource/get'
BOARD_INVITES_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardInvitesResource/get'
CREATE_COMMENT_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/create/'
GET_PIN_COMMENTS_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentFeedResource/get'
LOAD_PIN_URL_FORMAT = 'https://www.pinterest.com/pin/{}/'
DELETE_COMMENT = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/delete/'
CONVERSATION_RESOURCE = 'https://www.pinterest.com/resource/ConversationsResource/get/'
CONVERSATION_RESOURCE_CREATE = 'https://www.pinterest.com/resource/ConversationsResource/create/'
LOAD_CONVERSATION = 'https://www.pinterest.com/resource/ConversationMessagesResource/get/'
SEND_MESSAGE = 'https://www.pinterest.com/resource/ConversationMessagesResource/create/'
BOARD_SECTION_RESOURCE = 'https://www.pinterest.com/resource/BoardSectionResource/create/'
GET_BOARD_SECTIONS = 'https://www.pinterest.com/resource/BoardSectionsResource/get/'
BOARD_SECTION_EDIT_RESOURCE = 'https://www.pinterest.com/resource/BoardSectionEditResource/delete/'
GET_BOARD_SECTION_PINS = 'https://www.pinterest.com/resource/BoardSectionPinsResource/get/'
UPLOAD_IMAGE = 'https://www.pinterest.com/upload-image/'


class Pinterest:

    def __init__(self, password='', proxies=None, username='', email='', cred_root='data'):
        self.email = email
        self.username = username
        self.password = password
        self.req_builder = RequestBuilder()
        self.bookmark_manager = BookmarkManager()
        self.http = requests.session()
        self.proxies = proxies

        data_path = os.path.join(cred_root, self.email) + os.sep
        if not os.path.isdir(data_path):
            os.makedirs(data_path)

        self.registry = Registry('{}registry.dat'.format(data_path))

        cookies = self.registry.get(Registry.Key.COOKIES)
        if cookies is not None:
            self.http.cookies.update(cookies)

    def request(self, method, url, data=None, files=None, extra_headers=None):
        headers = CaseInsensitiveDict([
            ('Referer', HOME_PAGE),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Accept', 'application/json'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('User-Agent', AGENT_STRING)])
        csrftoken = self.http.cookies.get('csrftoken')
        if csrftoken:
            headers.update([('X-CSRFToken', csrftoken)])

        if extra_headers is not None:
            for h in extra_headers:
                headers.update([(h, extra_headers[h])])

        response = self.http.request(
            method, url, data=data, headers=headers, files=files, proxies=self.proxies)
        response.raise_for_status()
        self.registry.update(Registry.Key.COOKIES, response.cookies)
        return response

    def get(self, url):
        return self.request('GET', url=url)

    def post(self, url, data=None, files=None, headers=None):
        return self.request('POST', url=url, data=data, files=files, extra_headers=headers)

    def login(self):
        self.get(HOME_PAGE)
        self.get(LOGIN_PAGE)

        options = {
            'username_or_email': self.email,
            'password': self.password
        }

        data = self.req_builder.buildPost(
            options=options, source_url='/login/?referrer=home_page')
        return self.post(url=CREATE_USER_SESSION, data=data)

    def get_user_overview(self, username=None):
        if username is None:
            username = self.username

        options = {
            "isPrefetch": 'false',
            "username": username,
            "field_set_key": "profile"
        }
        url = self.req_builder.buildGet(url=USER_RESOURCE, options=options)
        result = self.get(url=url).json()

        return result['resource_response']['data']

    def home_feed(self, page_size=100):

        next_bookmark = self.bookmark_manager.get_bookmark(primary='home_feed')
        if next_bookmark == '-end-':
            return []

        options = {
            "bookmarks": [next_bookmark],
            "isPrefetch": False,
            "field_set_key": "hf_grid_partner",
            "in_nux": False,
            "prependPartner": True,
            "prependUserNews": False,
            "static_feed": False,
            "page_size": page_size
        }
        url = self.req_builder.buildGet(
            url=USER_HOME_FEED_RESOURCE, options=options)

        response = self.get(url=url).json()

        bookmark = '-end-'

        if 'bookmark' in response['resource_response']:
            bookmark = response['resource_response']['bookmark']

        self.bookmark_manager.add_bookmark(
            primary='home_feed', bookmark=bookmark)

        return response['resource_response']['data']
        
    def search(self, scope, query, page_size=50):

        next_bookmark = self.bookmark_manager.get_bookmark(primary='search', secondary=query)

        if next_bookmark == '-end-':
            return []

        terms = query.split(' ')
        escaped_query = "%20".join(terms)
        term_meta_arr = []
        for t in terms:
            term_meta_arr.append('term_meta[]=' + t)
        term_arg = "%7Ctyped&".join(term_meta_arr)
        source_url = '/search/{}/?q={}&rs=typed&{}%7Ctyped'.format(scope, escaped_query, term_arg)
        options = {
            "isPrefetch": False,
            "auto_correction_disabled": False,
            "query": query,
            "redux_normalize_feed": True,
            "rs": "typed",
            "scope": scope,
            "page_size": page_size,
            "bookmarks": [next_bookmark]
        }
        url = self.req_builder.buildGet(url=BASE_SEARCH_RESOURCE, options=options, source_url=source_url)
        resp = self.get(url=url).json()

        bookmark = resp['resource']['options']['bookmarks'][0]

        self.bookmark_manager.add_bookmark(primary='search', secondary=query, bookmark=bookmark)
        return resp['resource_response']['data']['results']
