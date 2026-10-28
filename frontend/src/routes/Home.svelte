<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'

    let question_list = [] 

    function get_question_list() {
        fastapi('get', '/api/question/list', {}, (json) => { 
            question_list = json
        })        
    }

    get_question_list()
</script>

<ul>
    {#each question_list as question}
        <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
    {/each}
    <!-- use:link 는 동일한 페이지라고 인식하기 때문에 서버로 페이지 요청을 보내지 않음 -->
</ul>