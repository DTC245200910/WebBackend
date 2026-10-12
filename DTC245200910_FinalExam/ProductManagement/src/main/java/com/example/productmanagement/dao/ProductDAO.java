package com.example.productmanagement.dao;

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
