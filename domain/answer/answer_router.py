from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud

router = APIRouter(
    prefix="/api/answer",
)

#POST 방식의 API 주소를 등록하는 데코레이터
#정상 처리 시 응답 본문 없이 HTTP 204 반환
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
#답변 등록 함수 정의
#_answer_create: 사용자가 입력한 답변 데이터를 담는 매개변수
def answer_create(question_id: int,
                    _answer_create: answer_schema.AnswerCreate,
                    db: Session = Depends(get_db)):

    # create answer
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    #db : DB 세션을 첫 번째 위치 인수로 전달
    #왼쪽은 호출받는 함수의 매개변수 이름, 오른쪽은 조회한 질문 객체
    #왼쪽은 호출받는 함수의 매개변수 이름, 오른쪽은 현재 함수에서 전달받은 답변 데이터
    answer_crud.create_answer(db, question=question,
                    answer_create=_answer_create)