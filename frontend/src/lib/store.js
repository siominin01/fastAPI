import { writable } from 'svelte/store' 

// persist (지속성)
// key : 저장할 이름 (예: "page") / initValue : 초기값 (예: 0)
const persist_storage = (key, initValue) => {
    // 브라우저의 localStorage에서 기존에 저장된 값을 가져온다.
    const storedValueStr = localStorage.getItem(key)
    // 저장된 값이 있으면 그 값을 사용하고, 없으면 초기값을 사용
    // JSON.parse() : 저장된 문자열을 원래 데이터형으로 변환
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    // subscribe() : 저장소의 값이 변경되는 것을 감지
    // 값이 변경되면 localStorage에 자동 저장
    // JSON.stringify() : 값을 저장할 수 있도록 JSON 문자열로 변환
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val)) 
    })
    return store
}

export const page = persist_storage("page", 0)