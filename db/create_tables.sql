CREATE TABLE IF NOT EXISTS lapgaps (
    DriverID SERIAL PRIMARY KEY,
    Driver VARCHAR(50) NOT NULL,
    LapTime DECIMAL(8, 3) NOT NULL,
    SpeedMode VARCHAR(20) NOT NULL,
    FullName VARCHAR(100) NOT NULL,
    TeamName VARCHAR(100) NOT NULL,
    TeamColor VARCHAR(10) NOT NULL,
    DriverNumber INT NOT NULL,
    Event VARCHAR(50) NOT NULL,
    GP VARCHAR(50) NOT NULL,
    Year INT NOT NULL
);


CREATE TABLE bestlapspeeds (
    Driver VARCHAR(3),
    Average_Speed INT,
    Maximum_Speed INT,
    Minimum_Speed INT,
    DriverNumber INT,
    TeamName VARCHAR(50),
    TeamColor VARCHAR(7),
    Event VARCHAR(50),
    GP VARCHAR(50),
    Year INT,
    id VARCHAR(36)
);


CREATE TABLE topspeed_st (
    Driver VARCHAR(3),
    LapNumber INT,
    SpeedST FLOAT,
    DriverNumber INT,
    TeamName VARCHAR(50),
    TeamColor VARCHAR(8),
    Event VARCHAR(50),
    GP VARCHAR(50),
    Year INT,
    id VARCHAR(36)
);

