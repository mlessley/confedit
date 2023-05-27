CREATE TABLE threshold_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    app VARCHAR(255),
    env VARCHAR(255),
    component VARCHAR(255),
    sub_component VARCHAR(255),
    threshold INT,
    active BOOLEAN DEFAULT TRUE,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

