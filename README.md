# git-lab-A50216: Quản lý phiên bản sản phẩm với Git & GitHub

**Phiên bản hiện tại**: `v1.0.1` (Hotfix)

Dự án bài tập thực hành môn Quản lý phiên bản sản phẩm (Git & GitHub).

## Thành viên nhóm
- **Sinh viên A**: KayND098 (MSSV: A50216)
- **Sinh viên B**: Collaborator

## Cấu trúc thư mục
- `app/`: Mã nguồn ứng dụng máy tính mini:
  - `calc.py`: Các hàm tính toán cơ bản (`add`, `sub`, `mul`, `div`).
  - `utils.py`: Các hàm tiện ích hỗ trợ định dạng số.
- `tests/`: Bộ kiểm thử tự động sử dụng thư viện `pytest`.
- `BAOCAO.md`: Báo cáo chi tiết các bước thực hành, ảnh chụp git log và trả lời câu hỏi tình huống.

## Hướng dẫn cài đặt và chạy kiểm thử
```bash
# Cài đặt thư viện kiểm thử pytest
pip install pytest

# Chạy toàn bộ unit test
pytest tests/
```
