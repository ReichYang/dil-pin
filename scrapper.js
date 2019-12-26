// import Axios from "axios";

// const { Builder, By, until } = require('selenium-webdriver');
// import catta from "catta";

let email;
let username
let password
let HOME_PAGE = 'https://www.pinterest.com/'
let AGENT_STRING = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"


email = 'yukunyang9508@gmail.com'
username = 'Yukunyang'
password = 'yyk828226'
    // let req_builder = RequestBuilder()
    // self.bookmark_manager = BookmarkManager()
    // self.http = requests.session()
    // self.proxies = proxies

async function log() {

    email = 'yukunyang9508@gmail.com'
    let source = 'https://www.pinterest.com/resource/UserSessionResource/create/?'

    let source_url = 'source_url=/login/?referrer=home_page'

    let data_pt1 = '&data=%7B%22options%22%3A%20%7B%22username_or_email%22%3A%20%22'
    let data_pt2 = '%22%2C%20%22password%22%3A%20%22'
    let data_pt3 = '%22%7D%2C%20%22context%22%3A%20null%7D&_='
    password = "yyk828226"

    let full_url = (source + encodeURIComponent(source_url) + data_pt1 + encodeURIComponent(email) + data_pt2 + encodeURIComponent(password) + data_pt3 + Date.now()).replace("%3D", "=")
    console.log(full_url)
    let headers = {
        'Referer': 'https://www.pinterest.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Access-Control-Allow-Origin': "*",
        'User-Agent': AGENT_STRING
    }
    const loginresp = catta.jsonp(
        full_url, {
            headers: {
                'Referer': 'https://www.pinterest.com/',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Access-Control-Allow-Origin': "*",
                'User-Agent': AGENT_STRING
            }
        }

    ).then((res) => console.log(res))

    // $http.jsonp(full_url)
}



$(document).ready(() => {
    log()
})

email = 'yukunyang9508@gmail.com'
let source = 'https://www.pinterest.com/resource/UserSessionResource/create/?'

let source_url = 'source_url=/login/?referrer=home_page'

let data_pt1 = '&data=%7B%22options%22%3A%20%7B%22username_or_email%22%3A%20%22'
let data_pt2 = '%22%2C%20%22password%22%3A%20%22'
let data_pt3 = '%22%7D%2C%20%22context%22%3A%20null%7D&_='
password = "yyk828226"

let full_url = (source + encodeURIComponent(source_url) + data_pt1 + encodeURIComponent(email) + data_pt2 + encodeURIComponent(password) + data_pt3 + Date.now()).replace("%3D", "=")
console.log(full_url)