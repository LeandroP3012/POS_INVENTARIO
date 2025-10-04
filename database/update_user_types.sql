-- =============================================================================
-- ACTUALIZACIÓN DE TIPOS DE USUARIO
-- =============================================================================
-- Agregar nuevos tipos de usuario al enum

USE pos_system;

-- Agregar los nuevos tipos al enum user_type
ALTER TABLE users MODIFY COLUMN user_type ENUM('admin', 'supervisor', 'manager', 'employee', 'cashier', 'user') DEFAULT 'user';

-- Verificar que se aplicó correctamente
DESCRIBE users;
