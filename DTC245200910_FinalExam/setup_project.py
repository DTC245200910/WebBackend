import os

# Định nghĩa cấu trúc thư mục và nội dung các file
project_structure = {
    "database.sql": """CREATE DATABASE IF NOT EXISTS product_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE product_db;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
    quantity INT NOT NULL
);

INSERT INTO products (name, price, quantity) VALUES
('Laptop Dell XPS 13', 25000000, 10),
('iPhone 15 Pro', 28000000, 15),
('Bàn phím cơ Keychron K2', 2200000, 30);
""",

    "pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>ProductManagement</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>war</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <version>6.0.0</version>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>jakarta.servlet.jsp</groupId>
            <artifactId>jakarta.servlet.jsp-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>jakarta.servlet.jsp.jstl</groupId>
            <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
            <version>3.0.0</version>
        </dependency>

        <dependency>
            <groupId>org.glassfish.web</groupId>
            <artifactId>jakarta.servlet.jsp.jstl</artifactId>
            <version>3.0.1</version>
        </dependency>

        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>8.3.0</version>
        </dependency>
    </dependencies>
</project>
""",

    "src/main/java/com/example/productmanagement/model/Product.java": """package com.example.productmanagement.model;

public class Product {
    private int id;
    private String name;
    private double price;
    private int quantity;

    public Product() {}

    public Product(String name, double price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    public Product(int id, String name, double price, int quantity) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public double getPrice() { return price; }
    public void setPrice(double price) { this.price = price; }

    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
}
""",

    "src/main/java/com/example/productmanagement/dao/ProductDAO.java": """package com.example.productmanagement.dao;

import com.example.productmanagement.model.Product;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProductDAO {
    private String jdbcURL = "jdbc:mysql://localhost:3306/product_db?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true";
    private String jdbcUsername = "root";
    private String jdbcPassword = "your_password"; // Đổi thành mật khẩu MySQL của bạn

    private static final String INSERT_PRODUCT_SQL = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?);";
    private static final String SELECT_PRODUCT_BY_ID = "SELECT id, name, price, quantity FROM products WHERE id = ?;";
    private static final String SELECT_ALL_PRODUCTS = "SELECT * FROM products;";
    private static final String DELETE_PRODUCT_SQL = "DELETE FROM products WHERE id = ?;";
    private static final String UPDATE_PRODUCT_SQL = "UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?;";

    protected Connection getConnection() {
        Connection connection = null;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(jdbcURL, jdbcUsername, jdbcPassword);
        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return connection;
    }

    public void insertProduct(Product product) {
        try (Connection connection = getConnection();
             PreparedStatement preparedStatement = connection.prepareStatement(INSERT_PRODUCT_SQL)) {
            preparedStatement.setString(1, product.getName());
            preparedStatement.setDouble(2, product.getPrice());
            preparedStatement.setInt(3, product.getQuantity());
            preparedStatement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public Product selectProduct(int id) {
        Product product = null;
        try (Connection connection = getConnection();
             PreparedStatement preparedStatement = connection.prepareStatement(SELECT_PRODUCT_BY_ID)) {
            preparedStatement.setInt(1, id);
            ResultSet rs = preparedStatement.executeQuery();
            if (rs.next()) {
                String name = rs.getString("name");
                double price = rs.getDouble("price");
                int quantity = rs.getInt("quantity");
                product = new Product(id, name, price, quantity);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return product;
    }

    public List<Product> selectAllProducts() {
        List<Product> products = new ArrayList<>();
        try (Connection connection = getConnection();
             PreparedStatement preparedStatement = connection.prepareStatement(SELECT_ALL_PRODUCTS)) {
            ResultSet rs = preparedStatement.executeQuery();
            while (rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                double price = rs.getDouble("price");
                int quantity = rs.getInt("quantity");
                products.add(new Product(id, name, price, quantity));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return products;
    }

    public boolean deleteProduct(int id) {
        boolean rowDeleted = false;
        try (Connection connection = getConnection();
             PreparedStatement statement = connection.prepareStatement(DELETE_PRODUCT_SQL)) {
            statement.setInt(1, id);
            rowDeleted = statement.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rowDeleted;
    }

    public boolean updateProduct(Product product) {
        boolean rowUpdated = false;
        try (Connection connection = getConnection();
             PreparedStatement statement = connection.prepareStatement(UPDATE_PRODUCT_SQL)) {
            statement.setString(1, product.getName());
            statement.setDouble(2, product.getPrice());
            statement.setInt(3, product.getQuantity());
            statement.setInt(4, product.getId());
            rowUpdated = statement.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rowUpdated;
    }
}
""",

    "src/main/java/com/example/productmanagement/controller/ProductServlet.java": """package com.example.productmanagement.controller;

import com.example.productmanagement.dao.ProductDAO;
import com.example.productmanagement.model.Product;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet("/")
public class ProductServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private ProductDAO productDAO;

    public void init() {
        productDAO = new ProductDAO();
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        String action = request.getServletPath();

        try {
            switch (action) {
                case "/new":
                    showNewForm(request, response);
                    break;
                case "/insert":
                    insertProduct(request, response);
                    break;
                case "/delete":
                    deleteProduct(request, response);
                    break;
                case "/edit":
                    showEditForm(request, response);
                    break;
                case "/update":
                    updateProduct(request, response);
                    break;
                default:
                    listProduct(request, response);
                    break;
            }
        } catch (Exception ex) {
            throw new ServletException(ex);
        }
    }

    private void listProduct(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        List<Product> listProduct = productDAO.selectAllProducts();
        request.setAttribute("listProduct", listProduct);
        RequestDispatcher dispatcher = request.getRequestDispatcher("product-list.jsp");
        dispatcher.forward(request, response);
    }

    private void showNewForm(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        RequestDispatcher dispatcher = request.getRequestDispatcher("product-form.jsp");
        dispatcher.forward(request, response);
    }

    private void showEditForm(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        int id = Integer.parseInt(request.getParameter("id"));
        Product existingProduct = productDAO.selectProduct(id);
        RequestDispatcher dispatcher = request.getRequestDispatcher("product-form.jsp");
        request.setAttribute("product", existingProduct);
        dispatcher.forward(request, response);
    }

    private void insertProduct(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        String name = request.getParameter("name");
        double price = Double.parseDouble(request.getParameter("price"));
        int quantity = Integer.parseInt(request.getParameter("quantity"));

        Product newProduct = new Product(name, price, quantity);
        productDAO.insertProduct(newProduct);
        response.sendRedirect("list");
    }

    private void updateProduct(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        int id = Integer.parseInt(request.getParameter("id"));
        String name = request.getParameter("name");
        double price = Double.parseDouble(request.getParameter("price"));
        int quantity = Integer.parseInt(request.getParameter("quantity"));

        Product product = new Product(id, name, price, quantity);
        productDAO.updateProduct(product);
        response.sendRedirect("list");
    }

    private void deleteProduct(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        int id = Integer.parseInt(request.getParameter("id"));
        productDAO.deleteProduct(id);
        response.sendRedirect("list");
    }
}
""",

    "src/main/webapp/product-list.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Quản Lý Sản Phẩm</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Danh Sách Sản Phẩm</h2>
        <a href="new" class="btn btn-primary">+ Thêm Sản Phẩm Mới</a>
    </div>

    <table class="table table-bordered table-striped align-middle">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Tên sản phẩm</th>
                <th>Giá (VNĐ)</th>
                <th>Số lượng</th>
                <th>Thao tác</th>
            </tr>
        </thead>
        <tbody>
            <c:forEach var="product" items="${listProduct}">
                <tr>
                    <td><c:out value="${product.id}" /></td>
                    <td><c:out value="${product.name}" /></td>
                    <td><c:out value="${product.price}" /></td>
                    <td><c:out value="${product.quantity}" /></td>
                    <td>
                        <a href="edit?id=${product.id}" class="btn btn-warning btn-sm">Sửa</a>
                        <a href="delete?id=${product.id}" 
                           class="btn btn-danger btn-sm" 
                           onclick="return confirm('Bạn có chắc chắn muốn xóa sản phẩm này không?');">Xóa</a>
                    </td>
                </tr>
            </c:forEach>
        </tbody>
    </table>

</body>
</html>
""",

    "src/main/webapp/product-form.jsp": """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title><c:if test="${product != null}">Sửa Sản Phẩm</c:if><c:if test="${product == null}">Thêm Sản Phẩm</c:if></title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4" style="max-width: 600px;">

    <div class="card">
        <div class="card-header bg-primary text-white">
            <h4>
                <c:if test="${product != null}">Chỉnh Sửa Thông Tin Sản Phẩm</c:if>
                <c:if test="${product == null}">Thêm Sản Phẩm Mới</c:if>
            </h4>
        </div>
        <div class="card-body">
            <form action="<c:if test='${product != null}'>update</c:if><c:if test='${product == null}'>insert</c:if>" method="post">
                
                <c:if test="${product != null}">
                    <input type="hidden" name="id" value="<c:out value='${product.id}' />" />
                </c:if>

                <div class="mb-3">
                    <label class="form-label">Tên sản phẩm:</label>
                    <input type="text" name="name" class="form-control" required value="<c:out value='${product.name}' />" />
                </div>

                <div class="mb-3">
                    <label class="form-label">Giá sản phẩm:</label>
                    <input type="number" step="0.01" name="price" class="form-control" required value="<c:out value='${product.price}' />" />
                </div>

                <div class="mb-3">
                    <label class="form-label">Số lượng:</label>
                    <input type="number" name="quantity" class="form-control" required value="<c:out value='${product.quantity}' />" />
                </div>

                <button type="submit" class="btn btn-success">Lưu lại</button>
                <a href="list" class="btn btn-secondary">Hủy</a>
            </form>
        </div>
    </div>

</body>
</html>
""",

    "src/main/webapp/WEB-INF/web.xml": """<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
         version="6.0">
</web-app>
""",

    "README.md": """# Hướng Dẫn Thực Hiện Bài Thi Cuối Module

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
"""
}

def create_project():
    root_dir = "ProductManagement"
    print(f"Đang khởi tạo dự án tại thư mục '{root_dir}'...")
    
    for filepath, content in project_structure.items():
        full_path = os.path.join(root_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" -> Đã tạo: {full_path}")
        
    print("\n[THÀNH CÔNG] Đã tạo toàn bộ file dự án!")
    print(f"Vào thư mục '{root_dir}' để kiểm tra hoặc nén thành file ZIP nộp bài.")

if __name__ == "__main__":
    create_project()