# BÁO CÁO BÀI TẬP VẬN DỤNG: GIT & GITHUB TRONG QUẢN LÝ PHIÊN BẢN SẢN PHẨM

- **Họ và tên Sinh viên A**: KayND098
- **Mã số sinh viên**: A50216
- **Link repository GitHub**: https://github.com/KayND098/A50216
- **Thành viên B**: Collaborator

---

## Chuẩn bị: Cấu hình Git một lần
Các lệnh cấu hình ban đầu:
```bash
git config --global pull.rebase true
git config --global rebase.autoStash true
```
**Giải thích**:
- `pull.rebase true`: Cấu hình mặc định cho lệnh `git pull` sẽ tự động thực hiện `rebase` thay vì tạo `merge commit`, giúp giữ lịch sử commit của nhánh thẳng và gọn gàng.
- `rebase.autoStash true`: Tự động cất các thay đổi dở dang (stash) trước khi bắt đầu rebase và tự động phục hồi (unstash) sau khi rebase hoàn tất, tránh xung đột working tree dở dang khi rebase.

---

## Phần A – Khởi tạo repo và quy ước nhóm (15 điểm)

### 1. Các lệnh đã thực hiện
```bash
# Khởi tạo repo và commit ban đầu trên main
git init
git add README.md .gitignore
git commit -m "chore: initial commit with README and python gitignore"
git branch -M main
git remote add origin https://github.com/KayND098/A50216.git
git push -u origin main

# Tạo và đẩy nhánh develop
git switch -c develop
git push -u origin develop

# Tạo nhánh tính năng feature/1-calc
git switch -c feature/1-calc
# Thêm file app/calc.py chứa hàm add(a, b) và sub(a, b)
git add app/calc.py
git commit -m "feat(calc): add add and sub functions"
git push -u origin feature/1-calc
```

### 2. Cấu hình bảo vệ nhánh (Branch Protection) trên GitHub
- Vào **Settings** -> **Branches** (hoặc **Rulesets**) trên GitHub:
  - Áp dụng cho: `main` và `develop`
  - Bật: **Require a pull request before merging** (Require approvals: 1)
  - Bật: **Do not allow bypass** / **Restrict pushes that create matching branches** (Cấm push trực tiếp)

### 3. Kiểm tra bảo vệ nhánh: Thử push trực tiếp lên develop
```bash
git switch develop
git commit --allow-empty -m "test: direct push to protected branch"
git push origin develop
```
**Thông báo lỗi nhận được từ GitHub**:
```text
remote: error: GH006: Protected branch update failed for refs/heads/develop.
remote: error: Changes must be made through a pull request.
remote: error: At least 1 approving review is required by reviewers with write access.
To https://github.com/KayND098/A50216.git
 ! [remote rejected] develop -> develop (protected branch hook declined)
error: failed to push some refs to 'https://github.com/KayND098/A50216.git'
```
**Giải thích**: GitHub đã kích hoạt hook bảo vệ nhánh. Nhánh `develop` được cấu hình bắt buộc mọi thay đổi phải thông qua Pull Request và có ít nhất 1 người phê duyệt, do đó thao tác push trực tiếp từ máy cục bộ bị server từ chối hoàn toàn.

### 4. Kết quả `git log --oneline --graph --all`
```text
* f6830ed (origin/feature/1-calc, feature/1-calc) feat(calc): add add and sub functions
* dcece19 (HEAD -> develop, origin/main, origin/develop, main) chore: initial commit with README and python gitignore
```
- **Link PR Squash Merge vào develop**: https://github.com/KayND098/A50216/pull/1

---

## Phần B – Đang code dở thì phải chuyển nhánh (15 điểm)

### 1. Thao tác thử chuyển nhánh khi chưa cất code
- Tạo nhánh `feature/2-mul` từ `develop`:
  ```bash
  git switch develop
  git switch -c feature/2-mul
  ```
- Viết dở hàm `mul(a, b)` trong `app/calc.py` và tạo file mới `app/utils.py` (chưa `git add`).
- Thử chuyển nhánh:
  ```bash
  git switch develop
  ```
- **Ghi nhận kết quả**:
  ```text
  Switched to branch 'develop'
  M	app/calc.py
  Your branch is up to date with 'origin/develop'.
  ```
  - Git cho phép chuyển nhánh vì trạng thái commit giữa `develop` và `feature/2-mul` hiện tại là giống nhau (chưa có commit xung đột).
  - Cả file đã sửa đổi `app/calc.py` (modified) và file mới `app/utils.py` (untracked) đều bị đem theo sang nhánh `develop`.

### 2. Cất toàn bộ việc dở (Stash) kể cả file untracked
```bash
git switch feature/2-mul
git stash push -u -m "WIP: implement mul and add utils"
```

### 3. Chứng minh working tree sạch và kiểm tra stash list
```bash
git status
# On branch feature/2-mul
# nothing to commit, working tree clean

git stash list
# stash@{0}: On feature/2-mul: WIP: implement mul and add utils
```

### 4. Sửa README qua nhánh fix/3-readme và PR
```bash
git switch develop
git switch -c fix/3-readme
# Chỉnh sửa nội dung README.md
git add README.md
git commit -m "docs(readme): fix incorrect usage instructions and add test guide"
git push -u origin fix/3-readme
# Mở Pull Request vào develop và merge
```

### 5. Quay lại feature/2-mul, lấy việc dở ra bằng apply và xóa stash
```bash
git switch feature/2-mul
git stash apply 'stash@{0}'
# Kiểm tra code còn nguyên vẹn
git status
# Xóa stash sau khi apply an toàn
git stash drop 'stash@{0}'
```

### 6. Trả lời câu hỏi Phần B
- **Nếu ở bước 2 quên `-u` thì điều gì xảy ra với `app/utils.py`?**
  Lệnh `git stash` mặc định chỉ lưu các thay đổi của những file đã được Git theo dõi (tracked files). File `app/utils.py` là untracked nên nếu thiếu `-u` (`--include-untracked`), nó sẽ bị bỏ lại trên working tree. Khi switch nhánh sang `develop`, file này sẽ bị đem theo sang nhánh `develop`, gây bẩn môi trường làm việc và có nguy cơ bị commit nhầm vào nhánh không liên quan.
- **Khi nào nên commit WIP thay vì stash?**
  - **Dùng stash khi**: Thay đổi nhỏ, dở dang cục bộ trên một máy, muốn làm sạch nhanh working tree để chuyển sang việc khác trong vài phút rồi quay lại lấy ra ngay.
  - **Dùng commit WIP khi**: Cần chuyển máy làm việc, cần sao lưu (push) lên GitHub để tránh mất dữ liệu khi hỏng máy, cần phối hợp với đồng nghiệp để review/hỗ trợ debug, hoặc khi khối lượng công việc dở dang quá lớn gồm nhiều file phức tạp.

---

## Phần C – Push bị từ chối và xung đột khi rebase (20 điểm)

### 1. Trình tự các bước mô phỏng xung đột
1. **A tạo nhánh và push hàm div ban đầu**:
   ```bash
   git switch develop
   git switch -c feature/4-div
   # Thêm hàm div báo lỗi "Khong chia duoc"
   git commit -am "feat(calc): add div function with error Khong chia duoc"
   git push -u origin feature/4-div
   ```
2. **B pull về, sửa thành "Loi: chia cho 0", commit và push trước**:
   ```bash
   git commit -am "fix(calc): change div error message to Loi: chia cho 0"
   git push origin feature/4-div
   ```
3. **A không pull, sửa cùng dòng thành "ZeroDivision", commit và push**:
   ```bash
   git commit -am "feat(calc): update div error message to ZeroDivision"
   git push origin feature/4-div
   ```
   **Lỗi nhận được**:
   ```text
   To https://github.com/KayND098/A50216.git
    ! [rejected]        feature/4-div -> feature/4-div (non-fast-forward)
   error: failed to push some refs to 'https://github.com/KayND098/A50216.git'
   hint: Updates were rejected because the tip of your current branch is behind
   hint: its remote counterpart. If you want to integrate the remote changes,
   hint: use 'git pull' before pushing again.
   hint: See the 'Note about fast-forwards' in 'git push --help' for details.
   ```
4. **Thử `git pull --no-rebase` trên một nhánh nháp để chụp log có merge commit**:
   ```bash
   git switch -c draft/4-div-merge
   git pull --no-rebase origin feature/4-div
   # Xử lý xung đột và commit
   git log --graph --oneline -n 6
   ```
   **Kết quả đồ thị commit (Lịch sử có Merge commit dạng mắt lưới)**:
   ```text
   *   709fc67 Merge branch 'feature/4-div' of origin into draft/4-div-merge
   |\  
   | * ff36549 fix(calc): change div error message to Loi: chia cho 0
   * | 9dfb6c0 feat(calc): update div error message to ZeroDivision
   |/  
   * b228533 feat(calc): add div function with error Khong chia duoc
   ```

5. **Trên nhánh thật `feature/4-div`: `git pull --rebase` và giải quyết xung đột**:
   ```bash
   git switch feature/4-div
   git pull --rebase origin feature/4-div
   ```
   - **Nội dung xung đột trong file `app/calc.py`**:
     ```python
     <<<<<<< HEAD (commit của B trên remote)
         if b == 0:
             raise ValueError("Loi: chia cho 0")
     =======
         if b == 0:
             raise ValueError("ZeroDivision")
     >>>>>>> feat(calc): update div error message to ZeroDivision
     ```
   - **Giải quyết xung đột**: Giữ thông báo của B và thêm mã lỗi của A:
     ```python
     if b == 0:
         raise ValueError("Loi: chia cho 0 (ZeroDivision)")
     ```
   - Tiếp tục rebase và push:
     ```bash
     git add app/calc.py
     git rebase --continue
     git push origin feature/4-div
     ```
   **Kết quả đồ thị commit sau Rebase (Lịch sử thẳng đẹp)**:
   ```text
   * bc73857 feat(calc): update div error message to ZeroDivision
   * ff36549 fix(calc): change div error message to Loi: chia cho 0
   * b228533 feat(calc): add div function with error Khong chia duoc
   ```

### 2. Biến thể bắt buộc: Hủy bỏ rebase (`git rebase --abort`)
- Khi gặp xung đột ở bước 5, nếu chạy:
  ```bash
  git rebase --abort
  ```
- **Mô tả trạng thái**: Quá trình rebase lập tức dừng lại, Git hoàn tác mọi trạng thái xung đột và trả working directory cũng như con trỏ HEAD về nguyên vẹn trạng thái trước khi gõ lệnh rebase (commit cục bộ của A vẫn giữ nguyên, nhánh chưa được đồng bộ với remote).

### 3. Biến thể force push: So sánh `--force` và `--force-with-lease`
- Giả sử A rebase `feature/4-div` lên `develop` mới nhất và cần đẩy lại lên remote:
  - **`git push --force` (`-f`)**: Ghi đè mù quáng toàn bộ lịch sử trên remote bằng lịch sử local. Nếu B vừa push một commit mới lên nhánh chung mà A chưa kịp fetch, commit của B sẽ bị xóa hoàn toàn khỏi remote.
  - **`git push --force-with-lease`**: Cơ chế an toàn hơn. Git sẽ kiểm tra xem ref trên remote có đúng bằng ref mà A đã fetch về lần gần nhất hay không. Nếu B đã push commit mới, Git sẽ từ chối thao tác force push và cảnh báo, giúp ngăn ngừa việc vô tình ghi đè code của người khác.

### 4. Trả lời câu hỏi Phần C
- **Trong lúc rebase, phía "ours" và "theirs" là code của ai?**
  - **`ours`**: Là code của commit trên upstream/remote (tức code của bạn B). Khi rebase, HEAD tạm thời được chuyển về đỉnh của upstream, nên upstream được coi là "của chúng ta" (ours).
  - **`theirs`**: Là commit đang được gắp và tua lại đè lên (replay onto), tức chính là code của bạn A (local commits). Khái niệm này bị ngược so với khi dùng `git merge`.
- **Vì sao không được rebase develop?**
  Nhánh `develop` là nhánh dùng chung công khai của cả team. Việc rebase sẽ viết lại lịch sử commit (thay đổi các commit hash). Nếu ai đó push force nhánh `develop` đã rebase lên remote, toàn bộ các thành viên khác đang làm việc dựa trên nhánh `develop` cũ sẽ bị xung đột nhánh phân kỳ nghiêm trọng, làm hỏng toàn bộ luồng tích hợp của dự án.

---

## Phần D – Cứu hộ commit (20 điểm)

| Sự cố | Mô tả sự cố | Lệnh khắc phục lựa chọn | Giải thích vì sao chọn lệnh đó |
|---|---|---|---|
| **D1** | Commit với message `"fix"` không mô tả gì | `git commit --amend -m "fix(calc): correctly format calculator error output"` | Vì commit này chưa được push lên remote, `git commit --amend` cho phép sửa trực tiếp message của commit gần nhất nhanh chóng và giữ lịch sử sạch đẹp. |
| **D2** | Lỡ `git add file .env` chứa mật khẩu giả | `git restore --staged .env`<br>Thêm `.env` vào `.gitignore` | `git restore --staged` đưa file ra khỏi Staging Area mà hoàn toàn không xóa hoặc làm mất nội dung trong working tree, sau đó đưa vào `.gitignore` để không bao giờ bị add lại. |
| **D3** | Commit tính năng `pow(a, b)` thẳng lên `develop` ở máy, chưa push | `git branch feature/5-pow`<br>`git reset --hard HEAD~1` (trên `develop`) | Lệnh `git branch` giữ lại commit vừa tạo trên nhánh mới `feature/5-pow`, sau đó `git reset --hard HEAD~1` trên `develop` đưa `develop` local quay về đúng vị trí sạch trùng khớp với remote. |
| **D4** | Một commit lỗi đã được merge và push lên `develop` | `git revert <commit_hash>`<br>Mở PR merge bản revert | Nhánh `develop` là nhánh dùng chung đã được push, tuyệt đối không dùng `reset` viết lại lịch sử. Dùng `git revert` tạo ra một commit mới đảo ngược thay đổi của commit lỗi, đảm bảo tính toàn vẹn của lịch sử chung. |
| **D5** | `git reset --hard HEAD~2` làm "mất" hai commit | 1. `git reflog`<br>2. Tìm commit hash trước khi reset<br>3. `git reset --hard <hash>` | `git reflog` ghi lại mọi di chuyển của con trỏ HEAD. Dù commit bị tách khỏi nhánh nhưng dữ liệu vẫn còn trong reflog, cho phép khôi phục chính xác trạng thái về trước lệnh reset. |

### Thử thách Cherry-pick
- Dùng `git cherry-pick ff36549` để đưa duy nhất một commit sửa lỗi từ `feature/4-div` sang một nhánh mới tách từ `develop` (ví dụ `fix/cherry-pick-div`), sau đó mở PR vào `develop` mà không kéo theo bất kỳ commit thừa nào khác.

---

## Phần E – Phát hành phiên bản và hotfix (15 điểm)

### 1. Quy trình phát hành bản `v1.0.0`
```bash
git switch develop
git switch -c release/1.0.0
# Cập nhật số phiên bản v1.0.0 vào README.md
git commit -am "chore(release): bump version to 1.0.0"
git push -u origin release/1.0.0
# Mở PR gộp release/1.0.0 vào main
# Gắn tag có chú thích trên main:
git switch main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0: Mini Calculator production ready"
git push origin v1.0.0
# Gộp ngược release/1.0.0 vào develop:
git switch develop
git merge release/1.0.0
git push origin develop
```

### 2. Quy trình Hotfix `v1.0.1`
- Phát hiện lỗi `div(1, 0)` trên bản production `v1.0.0`.
- Tạo nhánh hotfix tách trực tiếp từ tag `v1.0.0`:
  ```bash
  git checkout -b hotfix/1.0.1 v1.0.0
  # Sửa lỗi xử lý ngoại lệ trong app/calc.py (tránh crash)
  git commit -am "fix(calc): handle zero division safely with ZeroDivisionError (v1.0.1)"
  git push -u origin hotfix/1.0.1
  # Mở PR vào main, review và merge
  git switch main
  git pull origin main
  git tag -a v1.0.1 -m "Hotfix v1.0.1: Fix crash on zero division"
  git push origin v1.0.1
  # Đưa bản sửa hotfix vào develop:
  git switch develop
  git merge hotfix/1.0.1
  git push origin develop
  ```

### 3. Phát hành bản `v1.1.0`
- Bạn B hoàn thành tính năng `sqrt` trên `feature/6-sqrt` và merge vào `develop`.
- Merge `develop` vào `main` và gắn tag `v1.1.0`:
  ```bash
  git switch main
  git merge develop -m "chore(release): merge release 1.1.0 to main"
  git tag -a v1.1.0 -m "Release v1.1.0: Add sqrt function"
  git push origin main --tags
  ```

### 4. Trả lời câu hỏi Phần E
- **Vì sao hotfix tách từ tag chứ không tách từ develop?**
  Tag `v1.0.0` phản ánh chính xác mã nguồn đang chạy trên production. Nhánh `develop` lúc này đang chứa các tính năng mới dở dang (như `feature/6-sqrt`). Nếu tách hotfix từ `develop`, bản sửa lỗi sẽ kéo theo code chưa hoàn thiện lên production, gây nguy cơ phát sinh lỗi nghiêm trọng mới.
- **Nếu bỏ qua bước 6 thì bản `v1.1.0` gặp vấn đề gì?**
  Sẽ gặp lỗi hồi quy (regression bug). Nhánh `develop` sẽ không có bản sửa lỗi của hotfix `1.0.1`. Khi phát hành bản `1.1.0` từ `develop`, lỗi crash khi chia cho 0 sẽ lại xuất hiện trên production.
- **Giải thích vì sao bản có sqrt là MINOR còn bản sửa lỗi là PATCH?**
  Theo chuẩn Semantic Versioning (SemVer 2.0.0):
  - **PATCH**: Tăng khi phát hành các bản vá lỗi (bug fixes) tương thích ngược (backward compatible).
  - **MINOR**: Tăng khi bổ sung chức năng mới hoàn chỉnh (`sqrt`) nhưng vẫn giữ tính tương thích ngược với các hàm cũ.

---

## Phần F – Làm việc với AI agent trong Antigravity (10 điểm)

### 1. Quy trình thực hiện
1. Bảo đảm working tree sạch sẽ:
   ```bash
   git status
   git switch develop
   git switch -c feature/7-agent-tests
   ```
2. Yêu cầu AI Agent viết toàn bộ unit test cho `app/calc.py` bằng `pytest` trong file `tests/test_calc.py`.
3. Kiểm tra `git diff` trước khi commit.
   - **Ghi nhận điểm chỉnh sửa/từ chối**: Ban đầu AI agent sinh ra test case kiểm tra phép chia `div(a, 0)` nhưng sử dụng assert trả về `None` thay vì kiểm tra `pytest.raises(ZeroDivisionError)`. Tôi đã từ chối và sửa lại mã test để kiểm tra đúng ngoại lệ `ZeroDivisionError` theo đúng bản hotfix v1.0.1.
4. Chạy kiểm thử tự động xác nhận 100% test pass:
   ```bash
   pytest -v tests/test_calc.py
   # 8 passed in 0.05s
   ```
5. Commit với chuẩn Conventional Commits:
   ```bash
   git add tests/test_calc.py
   git commit -m "test(calc): add comprehensive pytest suite for all calculator operations"
   git push -u origin feature/7-agent-tests
   ```
6. Mở Pull Request vào `develop` và nhờ bạn cùng cặp review.

### 2. Trả lời câu hỏi Phần F
- **Những lệnh Git nào không nên giao cho agent tự chạy, và vì sao?**
  - `git push --force`, `git reset --hard`, `git clean -fdx`: Các lệnh này mang tính phá hủy dữ liệu, nếu agent thiếu ngữ cảnh có thể xóa vĩnh viễn commit hoặc file chưa kịp lưu.
  - `git rebase` giải quyết conflict logic nghiệp vụ: Agent có thể không hiểu rõ thỏa thuận giữa các thành viên, dẫn đến chọn sai nhánh code và làm hỏng logic phần mềm.
  - `git config --global`: Có thể làm thay đổi cấu hình máy của người dùng ngoài phạm vi repo.

---

## Câu hỏi tình huống (5 điểm)

### 1. Bạn chạy `git stash pop` và gặp xung đột. Stash còn hay đã mất? Bạn xử lý tiếp thế nào?
- **Trả lời**: Stash **vẫn còn nguyên** trong danh sách stash (Git không tự xóa stash khi gặp conflict để tránh mất mát dữ liệu).
- **Cách xử lý**:
  1. Mở file xung đột, xử lý các thẻ `<<<<<<<`, `=======`, `>>>>>>>`.
  2. Đánh dấu đã giải quyết bằng `git add <file>`.
  3. Hoàn tất việc xử lý, sau đó gõ lệnh xóa stash thủ công: `git stash drop`.

### 2. Một thành viên chạy `git push --force` lên develop và commit của bạn biến mất trên GitHub. Làm sao lấy lại, và cấu hình GitHub nào ngăn chuyện này?
- **Trả lời**:
  - **Cách lấy lại**:
    1. Kiểm tra trên máy local bằng `git reflog` để tìm lại commit SHA của commit bị mất.
    2. Checkout commit đó thành một nhánh mới: `git checkout -b restore-branch <commit_hash>`.
    3. Đẩy nhánh này lên GitHub và mở PR để merge lại vào `develop`.
  - **Cấu hình GitHub ngăn chặn**: Trong **Settings** -> **Branches** -> Quy tắc bảo vệ nhánh `develop`, bật tùy chọn **"Require a pull request before merging"**, bỏ chọn (không cho phép) **"Allow force pushes"**, và bật **"Include administrators"**.

### 3. Bạn đang rebase 5 commit và đến commit thứ 3 thì thấy commit đó không còn cần nữa. Lệnh nào phù hợp?
- **Trả lời**:
  - Chạy lệnh: `git rebase --skip`.
  - Lệnh này sẽ bỏ qua toàn bộ commit hiện tại đang gây xung đột / không cần thiết và tiếp tục áp dụng các commit còn lại.
  - (Nếu đang trong phiên interactive rebase `git rebase -i`, ta chỉ việc xóa dòng commit đó hoặc đổi từ `pick` sang `drop`).

### 4. Nhóm của bạn deploy web nhiều lần mỗi ngày. Bạn chọn Git Flow hay GitHub Flow? Lập luận.
- **Trả lời**:
  - **Lựa chọn**: **GitHub Flow**.
  - **Lập luận**:
    - Git Flow quá phức tạp với nhiều tầng nhánh (`main`, `develop`, `release/*`, `hotfix/*`), chu kỳ release nặng nề không phù hợp với việc deploy liên tục nhiều lần mỗi ngày (CI/CD).
    - GitHub Flow cực kỳ tinh gọn: Chỉ có nhánh `main` luôn sẵn sàng để deploy lên production. Mọi thay đổi đều được tạo nhánh ngắn hạn từ `main`, mở Pull Request, chạy kiểm thử tự động, review và merge vào `main` để deploy ngay lập tức.

### 5. Tag `v2.0.0` đã push nhưng gắn nhầm commit. Vì sao không nên xóa rồi gắn lại cùng tên, và nên làm gì thay thế?
- **Trả lời**:
  - **Vì sao không nên**: Tag công khai đã push lên remote thường được cache trên máy của các lập trình viên khác, trong hệ thống CI/CD và các package registry. Nếu xóa rồi gắn lại cùng tên `v2.0.0`, các máy đã tải tag cũ sẽ không tự động cập nhật tag mới, gây ra sự không nhất quán nghiêm trọng (cùng một tên tag nhưng trỏ tới hai mã commit khác nhau).
  - **Cách làm thay thế**: Giữ nguyên tag `v2.0.0` và phát hành ngay phiên bản mới tiếp theo theo chuẩn SemVer là `v2.0.1` (hoặc `v2.0.0-patch1`) trỏ đúng vào commit chuẩn, đồng thời ghi rõ trong Release Notes lý do cập nhật.
