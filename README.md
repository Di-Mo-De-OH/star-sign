# 🌟 별자리 궁합 서비스

> 고유 URL을 생성하고 참여자들의 생년월일을 입력받아 별자리 기반 궁합 점수와 관계도를 시각화하는 서비스

---

## 기술 스택

| 영역 | 기술 | 선택 이유 |
|------|------|-----------|
| Backend | Django REST Framework | Python 기반 빠른 API 개발, ORM 지원 |
| Frontend | React | 컴포넌트 기반 UI, 관계도 시각화에 적합 |
| Database | PostgreSQL | 안정적인 RDBMS, 복잡한 관계 쿼리 처리 |
| 인증 | JWT (SimpleJWT) | Stateless 인증, 모바일/웹 범용 |
| 배포 | AWS EC2 + Nginx + Gunicorn | 실서비스 수준 배포 환경 |
| 패키지 관리 | Poetry | 의존성 관리 및 가상환경 통합 관리 |

---

## 핵심 기능

- **URL 생성**: 로그인 유저가 고유 UUID 기반 URL을 발급받아 참여자에게 공유
- **URL 저장**: 로그인 유저는 본인이 생성한 URL 목록 조회 가능 (만료 후에도 조회 가능)
- **참여**: 비로그인 유저도 URL로 접속하여 참여 가능
- **별자리 자동 계산**: 생년월일 입력 시 별자리 자동 매핑
- **궁합 점수**: 참여자 간 0~100점 궁합 점수 계산
- **관계도 시각화**: 전체 참여자 궁합 관계도 표시
- **오늘의 운세**: 별자리별 일별 운세 제공
- **URL 만료**: 생성 후 24시간 이후 일반 접근 불가 (DB 데이터 유지)

---

## 시스템 아키텍처

```
Client (React)
    │
    │ HTTP
    ▼
Nginx
    │
    ▼
Gunicorn
    │
    ▼
Django REST Framework
    │         │
    ▼         ▼
PostgreSQL  Redis (JWT 블랙리스트)
```

---

## ERD

```
User
├── id
├── email
├── password
├── nickname
└── created_at

Link
├── id
├── host (FK → User)
├── uuid (고유 URL 키)
├── title
├── expires_at (생성 + 24시간)
└── created_at

Participant
├── id
├── link (FK → Link)
├── name
├── birth_date
├── zodiac (FK → Zodiac)
└── created_at

Compatibility
├── id
├── link (FK → Link)
├── participant_a (FK → Participant)
├── participant_b (FK → Participant)
└── score (0~100)

Zodiac
├── id
├── name (양자리, 황소자리 ...)
├── start_date
└── end_date

Fortune
├── id
├── zodiac (FK → Zodiac)
├── date
├── love (애정운)
├── money (금전운)
└── health (건강운)
```

---

## API 명세서

### 인증

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/v1/accounts/email/send` | 이메일 인증 코드 발송 |
| POST | `/api/v1/accounts/email/verify` | 이메일 인증 코드 검증 |
| POST | `/api/v1/accounts/signup` | 회원가입 |
| POST | `/api/v1/accounts/login` | 로그인 |
| POST | `/api/v1/accounts/logout` | 로그아웃 |

### URL 관리

| Method | URL | 설명 | 인증 |
|--------|-----|------|------|
| POST | `/api/v1/links` | URL 생성 | 필요 |
| GET | `/api/v1/links/{uuid}` | URL 조회 | 불필요 |
| GET | `/api/v1/links` | 내 URL 목록 조회 | 필요 |
| DELETE | `/api/v1/links/{uuid}` | URL 삭제 | 필요 |

### 참여자

| Method | URL | 설명 | 인증 |
|--------|-----|------|------|
| POST | `/api/v1/links/{uuid}/participants` | 참여자 등록 | 불필요 |
| GET | `/api/v1/links/{uuid}/participants` | 참여자 목록 조회 | 불필요 |

### 궁합

| Method | URL | 설명 | 인증 |
|--------|-----|------|------|
| GET | `/api/v1/links/{uuid}/compatibility` | 전체 궁합 관계도 조회 | 불필요 |

### 운세

| Method | URL | 설명 | 인증 |
|--------|-----|------|------|
| GET | `/api/v1/fortunes/{zodiac_id}/today` | 오늘의 운세 조회 | 불필요 |

---

## 실행 방법

```bash
# 의존성 설치
poetry install

# 환경변수 설정
cp .env.example .env

# 마이그레이션
poetry run python manage.py migrate

# 서버 실행
poetry run python manage.py runserver
```

---

## 프로젝트 구조

```
star-sign/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   ├── links/
│   ├── participants/
│   ├── compatibility/
│   ├── zodiac/
│   └── fortunes/
├── pyproject.toml
└── README.md
```
