from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

# JWT 액세스 토큰의 유효기간 (60분 × 24 = 1440분, 즉 24시간)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# JWT 서명에 사용하는 비밀키 (64자리 16진수 문자열)
SECRET_KEY = "0cc05c3f28a9377092c0fdfe1e0a6a86749d60625568a9d945f78fef260d3160"
# JWT 서명 알고리즘 (HS256: HMAC-SHA256)
ALGORITHM = "HS256"

# 사용자 관련 API의 공통 URL을 /api/user로 설정
router = APIRouter(
    prefix="/api/user",
)

# 회원가입 API: POST /api/user/create
# 회원가입 성공 시 응답 본문 없이 HTTP 204 반환
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 이미 등록된 사용자(아이디, 이메일 등)가 있는지 확인
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        # 중복된 사용자가 있으면 HTTP 409(충돌) 오류 반환
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    # 신규 사용자를 데이터베이스에 저장
    user_crud.create_user(db=db, user_create=_user_create)

# 로그인 API: POST /api/user/login
# 로그인 성공 시 Token 스키마 형식으로 응답
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # 1. 사용자 아이디와 비밀번호 확인
    # --------------------------------------------------

    # OAuth2PasswordRequestForm:
    # 로그인 요청으로 전달된 username과 password를 가져온다.
    # 입력 데이터는 JSON이 아닌 form 데이터 형식이다.

    # 입력받은 username으로 DB에서 사용자 정보 조회
    user = user_crud.get_user(db, form_data.username)
    # 사용자가 존재하지 않거나 비밀번호가 일치하지 않으면 인증 실패
    # pwd_context.verify(입력 비밀번호, DB에 저장된 해시 비밀번호)
    # 입력 비밀번호를 저장된 해시 방식으로 검증하여 일치 여부 판단
    # pwd_context.verify()는 단순히 두 문자열을 비교하는 함수가 아니라,
    # 입력한 비밀번호와 데이터베이스에 저장된 해시 비밀번호가 일치하는지 검증하는 함수
    if not user or not pwd_context.verify(form_data.password, user.password):
        # HTTP 401: 사용자 인증 실패 (Unauthorized)
        # WWW-Authenticate: Bearer > Bearer 토큰 인증 방식 사용 안내
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --------------------------------------------------
    # 2. JWT 액세스 토큰에 저장할 데이터 생성
    # --------------------------------------------------

    # JWT(JSON Web Token):
    # JSON 형식으로 사용자 정보 등을 담아 전달하는 토큰
    # Claim(클레임)은 JWT에 저장되는 정보의 항목을 의미한다.
    #
    # sub (Subject): 토큰의 주체, 여기서는 사용자 아이디
    # exp (Expiration Time): 토큰의 만료 시간
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    } # 현재 UTC 시간 + 24시간

    # --------------------------------------------------
    # 3. JWT 액세스 토큰 생성
    # --------------------------------------------------

    # jwt.encode(데이터, 비밀키, 서명 알고리즘)
    # data에 담긴 사용자 정보와 만료 시간을 이용해 JWT 생성
    # SECRET_KEY와 HS256 알고리즘으로 디지털 서명한다.
    # JWT는 기본적으로 암호화가 아닌 인코딩과 서명을 사용한다.
    # jwt.encode()는 사용자 정보를 암호화해 숨기는 함수가 아니라,
    # JWT를 생성하고 서명하여 위변조를 검증할 수 있도록 만드는 함수
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


    # --------------------------------------------------
    # 4. 로그인 성공 결과 반환
    # --------------------------------------------------

    # access_token: 생성된 JWT 토큰
    # token_type: 인증 방식 (Bearer: 베어러)
    # username: 로그인한 사용자 아이디
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }