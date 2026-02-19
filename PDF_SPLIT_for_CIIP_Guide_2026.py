import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter


# =========================
# 1) 여기만 필요시 수정
# =========================
SECTIONS = [
    ("I_Unix_서버", 7),
    ("II_Windows_서버", 172),
    ("III_웹_서비스", 271),
    ("IV_보안_장비", 353),
    ("V_네트워크_장비", 387),
    ("VI_제어시스템", 467),
    ("VII_PC", 552),
    ("VIII_DBMS", 593),
    ("IX_이동통신", 670),
    ("X_Web_Application(웹)", 676),
    ("XI_가상화_장비", 787),
    ("XII_클라우드", 851),
]

# 목차 인쇄 페이지번호와 PDF 실제 페이지가 어긋나면 조정 (한 번 맞추면 끝)
PAGE_OFFSET = 0
# =========================


def safe_filename(name: str) -> str:
    bad = r'\/:*?"<>|'
    for ch in bad:
        name = name.replace(ch, "_")
    return name.strip()


def split_pdf_by_sections(pdf_path: str, out_dir: str):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    # 섹션 시작 페이지(인쇄 기준)를 PDF 인덱스(0-based)로 변환
    # 인쇄페이지 1 -> index 0 이므로: index = (page_no + offset) - 1
    starts = []
    for title, start_page in SECTIONS:
        start_index = (start_page + PAGE_OFFSET) - 1
        starts.append((title, start_page, start_index))

    # 정렬(혹시라도 안전)
    starts.sort(key=lambda x: x[2])

    # 범위 계산: [start_index, next_start_index-1]
    ranges = []
    for i in range(len(starts)):
        title, start_page, start_idx = starts[i]
        if i < len(starts) - 1:
            next_start_idx = starts[i + 1][2]
            end_idx = next_start_idx - 1
        else:
            end_idx = total_pages - 1

        ranges.append((title, start_page, start_idx, end_idx))

    # 유효성 체크 + 저장
    saved = []
    for title, start_page, start_idx, end_idx in ranges:
        # 경계 보정
        if start_idx < 0:
            start_idx = 0
        if end_idx >= total_pages:
            end_idx = total_pages - 1

        if start_idx > end_idx:
            # 오프셋이 크게 틀렸거나 목차 페이지가 잘못된 경우
            continue

        writer = PdfWriter()
        for p in range(start_idx, end_idx + 1):
            writer.add_page(reader.pages[p])

        filename = f"{safe_filename(title)}_{start_page}p_to_{(end_idx + 1 - PAGE_OFFSET)}p.pdf"
        out_path = os.path.join(out_dir, filename)

        with open(out_path, "wb") as f:
            writer.write(f)

        saved.append((title, start_idx + 1, end_idx + 1, out_path))

    return total_pages, saved


def main():
    root = tk.Tk()
    root.withdraw()

    pdf_path = filedialog.askopenfilename(
        title="분리할 PDF 선택",
        filetypes=[("PDF files", "*.pdf")],
    )
    if not pdf_path:
        return

    base = os.path.splitext(os.path.basename(pdf_path))[0]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = filedialog.askdirectory(title="저장 폴더 선택")
    if not out_dir:
        return

    out_dir = os.path.join(out_dir, f"{base}_SPLIT_{ts}")
    os.makedirs(out_dir, exist_ok=True)

    try:
        total_pages, saved = split_pdf_by_sections(pdf_path, out_dir)

        if not saved:
            messagebox.showerror(
                "실패",
                "저장된 파일이 없습니다.\nPAGE_OFFSET이 맞는지 확인해 주세요.",
            )
            return

        # 결과 요약
        lines = [f"- 총 페이지: {total_pages}",
                 f"- 저장 폴더: {out_dir}",
                 "",
                 "[저장 결과]"]
        for title, s, e, path in saved:
            lines.append(f"• {title}: PDF {s}~{e} 페이지 -> {os.path.basename(path)}")

        messagebox.showinfo("완료", "\n".join(lines))

    except Exception as e:
        messagebox.showerror("에러", str(e))


if __name__ == "__main__":
    main()
