
-- ============================================
-- SAMPLE DATA
-- ============================================

-- Departments
INSERT INTO departments
    (department_name, description)
VALUES
    ('General Medicine',
     'General health consultation');

INSERT INTO departments
    (department_name, description)
VALUES
    ('Cardiology',
     'Heart and cardiovascular care');

INSERT INTO departments
    (department_name, description)
VALUES
    ('Dermatology',
     'Skin and related conditions');

INSERT INTO departments
    (department_name, description)
VALUES
    ('Pediatrics',
     'Healthcare for children');

-- Doctors
INSERT INTO doctors
    (department_id, doctor_name, specialization, email, phone)
SELECT department_id,
       'Dr. Aarav Sharma',
       'General Physician',
       'aarav.sharma@health.com',
       '9800000001'
FROM departments
WHERE department_name = 'General Medicine';

INSERT INTO doctors
    (department_id, doctor_name, specialization, email, phone)
SELECT department_id,
       'Dr. Priya Thapa',
       'Cardiologist',
       'priya.thapa@health.com',
       '9800000002'
FROM departments
WHERE department_name = 'Cardiology';

INSERT INTO doctors
    (department_id, doctor_name, specialization, email, phone)
SELECT department_id,
       'Dr. Rohan Singh',
       'Dermatologist',
       'rohan.singh@health.com',
       '9800000003'
FROM departments
WHERE department_name = 'Dermatology';

-- Patients
INSERT INTO patients
    (patient_name, date_of_birth, gender, email, phone, address)
VALUES
    ('Amresh Yadav',
     DATE '2002-05-15',
     'Male',
     'amresh@example.com',
     '9810000001',
     'Kathmandu, Nepal');

INSERT INTO patients
    (patient_name, date_of_birth, gender, email, phone, address)
VALUES
    ('Sita Sharma',
     DATE '1998-08-20',
     'Female',
     'sita@example.com',
     '9810000002',
     'Lalitpur, Nepal');

INSERT INTO patients
    (patient_name, date_of_birth, gender, email, phone, address)
VALUES
    ('Raj Kumar',
     DATE '1995-02-10',
     'Male',
     'raj@example.com',
     '9810000003',
     'Bhaktapur, Nepal');

COMMIT;

-- Check records
SELECT * FROM departments;
SELECT * FROM doctors;
SELECT * FROM patients;