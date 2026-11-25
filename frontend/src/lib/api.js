import qs from "qs"
import { access_token, username, is_login } from "./store"
import { get } from "svelte/store"
import { push } from "svelte-spa-router"

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    // get, post, put, delete 
    let content_type = 'application/json'
    // 서버에 보내는 데이터의 형식이 JSON이라고 알려주기 위한 값
    let body = JSON.stringify(params)
    // 자바스크립트 객체를 JSON 문자열로 변환

    if(operation === 'login') { 
        method = 'post'
        content_type = 'application/x-www-form-urlencoded' 
        body = qs.stringify(params)
    }

    // let _url = 'http://127.0.0.1:8000'+url 
    let _url = import.meta.env.VITE_SERVER_URL+url
    // API 호출 주소는 호스트명 (예: http://127.0.0.1:8000)에 전달받은 url 값 (라우터)
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params) 
    }

    let options = { 
        method: method, 
        headers: {
            "Content-Type": content_type 
        }
    }

    // 스토어 변수의 값을 읽으려면 get 함수를 사용해야 하고
    // 아래 fatch API에서 처럼 값을 저장할때는 acess_token.set처럼 set 함수를 사용
    const _access_token = get(access_token)
    if (_access_token) { // acess_token에 값ㅇ디 있을 경우에 HTTP 헤더에 Authorization 항목을 추가
        options.headers["Authorization"] = "Bearer " + _access_token
        // Authorization 헤더 항목의 값은 "Bearer" 문자열에 띄어쓰기 한 후에 엑세스 토큰ㅇ르 더하여 만들어야 함
    }

    if (method !== 'get') { 
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if(response.status === 204) { // No content 
                if(success_callback) {
                    success_callback() 
                }
                return
            }            
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) { 
                            success_callback(json)
                        }
                    // 알림 메세지를 보여주고 로그인 화면으로 이동 그리고 사용자 정보도 모두 초기화
                    } else if(operation !== 'login' && response.status === 401) { // token time out
                        access_token.set('')
                        username.set('')
                        is_login.set(false)
                        alert("로그인이 필요합니다")
                        push('/user-login')
                    } else {
                        if (failure_callback) { 
                            failure_callback(json)
                        } else {
                            alert(JSON.stringify(json)) 
                        }
                    } 
                })
                .catch(error => {
                    alert(JSON.stringify(error)) 
                })
        })
    }

export default fastapi