# Hướng Dẫn Thực Hiện Bài Thi Cuối Module

## 1. Khởi tạo Cơ sở dữ liệu
Chạy file `database.sql` trong MySQL để tạo database `product_db` và bảng `products`.

## 2. Cấu hình Mật khẩu Database
Mở file `src/main/java/com/example/productmanagement/dao/ProductDAO.java` và sửa lại `jdbcPassword` đúng với mật khẩu MySQL của bạn.

## 3. Chạy Dự án
1. Mở thư mục dự án trong IntelliJ IDEA / Eclipse.
2. Cấu hình Apache Tomcat (phiên bản 10 trở lên hỗ trợ Jakarta EE).
3. Chạy ứng dụng và truy cập: `http://localhost:8080/ProductManagement/`

## 4. Đóng gói Nộp bài
Nén toàn bộ thư mục này thành file `.zip` theo tên: `[Mã_số_sinh_viên]_FinalExam.zip`.
