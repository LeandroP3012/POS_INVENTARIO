-- =============================================================================
-- AGREGAR TABLA user_sessions AL SISTEMA POS
-- =============================================================================

USE pos_system;

-- Crear tabla de sesiones de usuarios
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    login_method VARCHAR(20) DEFAULT 'manual',
    logout_reason VARCHAR(50) NULL,
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSON,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_is_active (is_active),
    INDEX idx_expires_at (expires_at),
    INDEX idx_login_time (login_time),
    INDEX idx_last_activity (last_activity),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Sesiones de usuarios activas';

-- Verificar que la tabla se creó correctamente
SELECT 'Tabla user_sessions creada exitosamente!' as resultado;
DESCRIBE user_sessions;
