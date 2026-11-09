from datetime import datetime
from domain.question.question_schema import QuestionCreate
from models import Question
from sqlalchemy.orm import Session

# skip은 조회한 데이터의 시작위치를 의미
# 300 개의 데이터 중에서 21 ~ 30 번째 데이터를 가져오려면 skip은 20, limit 는 10
def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question)\
    .order_by(Question.create_date.desc())
    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate):
    db_question = Question(subject=question_create.subject, \
                            content=question_create.content, \
                            create_date=datetime.now())
    db.add(db_question)
    db.commit()