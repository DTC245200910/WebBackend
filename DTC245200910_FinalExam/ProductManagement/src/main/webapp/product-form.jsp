<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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
