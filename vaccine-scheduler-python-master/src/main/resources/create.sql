CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

--11/18/2024
CREATE TABLE Patients (
    Username VARCHAR(255) PRIMARY KEY,
    Salt BINARY(16),
    Hash BINARY(16)
);

CREATE TABLE Reservations (
    AppointmentID INT IDENTITY(1,1) PRIMARY KEY,
    Date DATE,
    VaccineName VARCHAR(255) REFERENCES Vaccines(Name),
    PatientUsername VARCHAR(255) REFERENCES Patients(Username),
    CaregiverUsername VARCHAR(255) REFERENCES Caregivers(Username)
);
