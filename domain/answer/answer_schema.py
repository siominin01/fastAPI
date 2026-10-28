import datetime
from pydantic import BaseModel, field_validator

class AnswerCreate(BaseModel):
    content: str

    #content 필드의 값을 검사하도록 지정
    @field_validator('content')
    #유효성 검사 함수 정의
    #이 함수가 속한 클래스 (AnswerCreate)
    #검사할 content 필드의 값
    def not_empty(cls, v):
        #값이 비어 있는지 검사
        #공백을 제거했을 때 빈 문자열인지 검사
        if not v or not v.strip():
            #검사에 실패하면 오류 발생
            raise ValueError('빈 값은 허용되지 않습니다 .')
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
