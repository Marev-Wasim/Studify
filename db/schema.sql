USE Studify_db;
GO

-- 1. Users
-- IDENTITY(1,1): auto-incrementing column that starts at 1 (seed) and increases by 1 (step size) for each new row
-- commonly used for primary keys
-- UNIQUE: ensure that all values in the specified column are distinct, no two rows can have the same value(s) in those columns
-- password hash: a one-way, irreversible transformation of a password into a unique string of characters
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    total_coins INT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 2. Subjects
-- ON DELETE CASCADE: a foreign key constraint that automatically deletes rows in a child table when the corresponding row in the parent table is deleted
CREATE TABLE subjects (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    name NVARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
GO

-- 3. Study Logs
-- DECIMAL(4,2): a data type that specifies a number with a total of four digits, where two of those digits are after the decimal point
CREATE TABLE study_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    study_date DATE NOT NULL,
    hours_studied DECIMAL(4,2) NOT NULL CHECK (hours_studied > 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE NO ACTION
);
GO

-- 4. Coin Transactions
-- reason: to earn money, auto-filled through Flask
CREATE TABLE coin_transactions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    study_log_id INT,
    coins_earned INT NOT NULL,
    reason NVARCHAR(200),
    transaction_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE NO ACTION,
    FOREIGN KEY (study_log_id) REFERENCES study_logs(id) ON DELETE SET NULL
);
GO

-- 5. Friends
-- The table only prevents duplicate or self-friend entries
-- Guarantees that (2,5) and (5,2) can’t both exist
CREATE TABLE friends (
    user_id1 INT NOT NULL,
    user_id2 INT NOT NULL,
    status NVARCHAR(20) DEFAULT 'pending', -- pending, accepted, rejected
    requested_at DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (user_id1, user_id2),
    FOREIGN KEY (user_id1) REFERENCES users(id) ON DELETE NO ACTION,
    FOREIGN KEY (user_id2) REFERENCES users(id) ON DELETE NO ACTION,
    CHECK (user_id1 < user_id2) -- store the smaller user ID first, prevents a user from friending themselves
);
GO

-- Indexes for performance
CREATE INDEX idx_study_logs_user_date ON study_logs(user_id, study_date);
CREATE INDEX idx_friends_user ON friends(user_id1, status);
CREATE INDEX idx_study_logs_user_subject ON study_logs(user_id, subject_id);
GO

PRINT 'All 5 tables created successfully!';