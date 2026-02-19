# PDF_SPLIT_for_CIIP_Guide_2026

CIIP 가이드 PDF를 섹션별로 자동 분할하는 간단한 GUI 도구입니다. 미리 정의한 섹션 시작 페이지를 기준으로 PDF를 여러 파일로 나눕니다.

**주요 기능**
- Tkinter 파일 선택창으로 입력 PDF와 출력 폴더를 선택
- 섹션 시작 페이지 목록(`SECTIONS`)을 기준으로 자동 분할
- 결과를 타임스탬프가 포함된 하위 폴더에 저장
- 파일명 자동 정리(금지 문자 치환)

**동작 방식**
1. 입력 PDF 선택
2. 출력 폴더 선택
3. `SECTIONS`의 시작 페이지 기준으로 구간 계산
4. 각 구간을 개별 PDF로 저장

**요구 사항**
- Python 3
- 패키지: `PyPDF2`

설치:
```bash
pip install PyPDF2
```

실행:
```bash
python PDF_SPLIT_for_CIIP_Guide_2026.py
```

**설정(필수 수정 포인트)**
- `SECTIONS`: 섹션 이름과 시작 페이지 번호의 목록
- `PAGE_OFFSET`: 목차 페이지 번호와 실제 PDF 페이지 번호가 다를 때 보정 값

예시 규칙:
- `SECTIONS`의 시작 페이지는 **목차 기준 페이지**
- 실제 PDF 페이지와 어긋나면 `PAGE_OFFSET`을 조정

**출력 형식**
- 출력 폴더: `원본파일명_SPLIT_YYYYMMDD_HHMMSS`
- 출력 파일명: `{섹션명}_{시작페이지}p_to_{끝페이지}p.pdf`

**주의 사항**
- PDF는 `.gitignore`로 전체 제외되어 있어 Git에 올라가지 않습니다.
- 섹션명에 특수문자가 있으면 자동으로 `_`로 치환됩니다.

**파일**
- `PDF_SPLIT_for_CIIP_Guide_2026.py`: 메인 스크립트
