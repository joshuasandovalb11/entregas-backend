-- Script para insertar datos ficticios básicos en la base de datos EntregasAppDB_Test
-- DIRECCIONES DE TIJUANA - Solo datos básicos, sin información que genera el sistema
-- EJECUTAR EN SQL SERVER MANAGEMENT STUDIO

USE EntregasAppDB_Test;
GO

-- Limpiar datos existentes (si los hay)
DELETE FROM tracking_points;
DELETE FROM deliveries;
DELETE FROM fecs;
DELETE FROM clients;
DELETE FROM salespersons;
DELETE FROM drivers;

-- Resetear los contadores de identidad
DBCC CHECKIDENT ('tracking_points', RESEED, 0);
DBCC CHECKIDENT ('deliveries', RESEED, 0);
DBCC CHECKIDENT ('fecs', RESEED, 0);
DBCC CHECKIDENT ('clients', RESEED, 0);
DBCC CHECKIDENT ('salespersons', RESEED, 0);
DBCC CHECKIDENT ('drivers', RESEED, 0);

-- 1. INSERTAR CONDUCTORES (Drivers)
-- Solo datos básicos del conductor, sin contraseñas reales
INSERT INTO drivers (username, hashed_password, num_unity, vehicle_plate, phone_number) VALUES
('carlos.rodriguez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBRLtdHIQABOVm', 'UN001', 'TIJ-001', '6641234567'),
('maria.gonzalez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBRLtdHIQABOVm', 'UN002', 'TIJ-002', '6642345678'),
('jose.martinez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBRLtdHIQABOVm', 'UN003', 'TIJ-003', '6643456789'),
('ana.lopez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBRLtdHIQABOVm', 'UN004', 'TIJ-004', '6644567890'),
('pedro.sanchez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBRLtdHIQABOVm', 'UN005', 'TIJ-005', '6645678901');

-- 2. INSERTAR VENDEDORES (Salespersons)
INSERT INTO salespersons (name, phone) VALUES
('Joshua Sandoval', '6647099372'),
('Carmen Jiménez', '6642223344'),
('Manuel Torres', '6643334455'),
('Sofía Herrera', '6644445566'),
('Diego Morales', '6645556677'),
('Isabella Cruz', '6646667788'),
('Fernando Ruiz', '6647778899');

-- 3. INSERTAR CLIENTES (Clients) - DIRECCIONES DE TIJUANA
INSERT INTO clients (name, phone, gps_location, salesperson_id) VALUES
-- Zona Centro - Vendedor Roberto Vargas (ID: 1)
('Supermercado La Frontera', '6641001001', '32.5149,-117.0382', 1),
('Panadería Doña Rosa', '6641001002', '32.5167,-117.0401', 1),
('Ferretería El Norte', '6641001003', '32.5134,-117.0365', 1),
('Farmacia Revolución', '6641001004', '32.5156,-117.0389', 1),

-- Zona Río - Vendedor Carmen Jiménez (ID: 2)  
('Restaurante Mariscos El Calamar', '+52664200-2001', '32.5321,-117.0182', 2),
('Plaza Río Tijuana', '+52664200-2002', '32.5285,-117.0156', 2),
('Hotel Lucerna Tijuana', '+52664200-2003', '32.5298,-117.0173', 2),
('Oficinas Corporativas Del Río', '+52664200-2004', '32.5312,-117.0189', 2),

-- Zona Mesa de Otay - Vendedor Manuel Torres (ID: 3)
('Centro Comercial Macroplaza', '+52664300-3001', '32.5589,-116.9821', 3),
('Hospital Ángeles Tijuana', '+52664300-3002', '32.5612,-116.9845', 3),
('Universidad CETYS Campus Tijuana', '+52664300-3003', '32.5567,-116.9798', 3),

-- Zona Playas - Vendedor Sofía Herrera (ID: 4)
('Hotel Real del Río', '+52664400-4001', '32.5678,-117.1234', 4),
('Restaurante La Diferencia', '+52664400-4002', '32.5656,-117.1267', 4),
('Clínica Hospital Playas', '+52664400-4003', '32.5689,-117.1201', 4),

-- Zona La Mesa - Vendedor Diego Morales (ID: 5)
('Soriana La Mesa', '+52664500-5001', '32.5234,-116.9876', 5),
('Gasolinera PEMEX La Mesa', '+52664500-5002', '32.5267,-116.9845', 5),

-- Zona Otay Centenario - Vendedor Isabella Cruz (ID: 6)
('Preparatoria Federal Lázaro Cárdenas', '+52664600-6001', '32.5445,-116.9234', 6),
('Centro de Salud Otay', '+52664600-6002', '32.5478,-116.9267', 6),

-- Zona Aeropuerto - Vendedor Fernando Ruiz (ID: 7)
('Hotel City Express Tijuana', '+52664700-7001', '32.5423,-116.9678', 7),
('Laboratorio Chopo Aeropuerto', '+52664700-7002', '32.5401,-116.9645', 7);

-- 4. INSERTAR FECs (con fec_number como INT)
-- Solo información básica del FEC, sin datos de optimización que genera el sistema
INSERT INTO fecs (fec_number, fec_date, status, driver_id, optimized_order_list_json, suggested_journey_polyline) VALUES
-- FECs para hoy y días siguientes - Solo datos básicos
(20250115, '2025-01-15', 'active', 1, NULL, NULL),
(20250115, '2025-01-15', 'active', 2, NULL, NULL),
(20250115, '2025-01-15', 'active', 3, NULL, NULL),
(20250116, '2025-01-16', 'active', 4, NULL, NULL),
(20250116, '2025-01-16', 'active', 5, NULL, NULL),
(20250117, '2025-01-17', 'pending', 1, NULL, NULL),
(20250117, '2025-01-17', 'pending', 2, NULL, NULL);

-- 5. INSERTAR ENTREGAS (Deliveries)
-- Solo datos básicos necesarios para crear la entrega
-- Todos los campos que llena el sistema (tiempos, duraciones, coordenadas finales) van como NULL
INSERT INTO deliveries (
    fec_id, driver_id, client_id, invoice_id, status, priority, 
    start_time, delivery_time, accepted_next_at,
    actual_duration, estimated_duration,
    start_latitud, start_longitud, end_latitud, end_longitud, distance,
    cancellation_reason, cancellation_notes
) VALUES
-- Entregas para FEC 20250115 - Carlos Rodriguez (Centro)
(1, 1, 1, 'INV-2025-001', 'pending', 1, '2025-01-15 08:00:00', NULL, NULL, NULL, NULL, 32.5149, -117.0382, NULL, NULL, NULL, NULL, NULL),
(1, 1, 2, 'INV-2025-002', 'pending', 2, '2025-01-15 09:00:00', NULL, NULL, NULL, NULL, 32.5167, -117.0401, NULL, NULL, NULL, NULL, NULL),
(1, 1, 3, 'INV-2025-003', 'pending', 3, '2025-01-15 10:00:00', NULL, NULL, NULL, NULL, 32.5134, -117.0365, NULL, NULL, NULL, NULL, NULL),
(1, 1, 4, 'INV-2025-004', 'pending', 4, '2025-01-15 11:00:00', NULL, NULL, NULL, NULL, 32.5156, -117.0389, NULL, NULL, NULL, NULL, NULL),

-- Entregas para FEC 20250115 - Maria Gonzalez (Zona Río)
(2, 2, 5, 'INV-2025-005', 'pending', 1, '2025-01-15 08:30:00', NULL, NULL, NULL, NULL, 32.5321, -117.0182, NULL, NULL, NULL, NULL, NULL),
(2, 2, 6, 'INV-2025-006', 'pending', 2, '2025-01-15 09:30:00', NULL, NULL, NULL, NULL, 32.5285, -117.0156, NULL, NULL, NULL, NULL, NULL),
(2, 2, 7, 'INV-2025-007', 'pending', 3, '2025-01-15 10:30:00', NULL, NULL, NULL, NULL, 32.5298, -117.0173, NULL, NULL, NULL, NULL, NULL),
(2, 2, 8, 'INV-2025-008', 'pending', 4, '2025-01-15 11:30:00', NULL, NULL, NULL, NULL, 32.5312, -117.0189, NULL, NULL, NULL, NULL, NULL),

-- Entregas para FEC 20250115 - Jose Martinez (Mesa de Otay)
(3, 3, 9, 'INV-2025-009', 'pending', 1, '2025-01-15 08:45:00', NULL, NULL, NULL, NULL, 32.5589, -116.9821, NULL, NULL, NULL, NULL, NULL),
(3, 3, 10, 'INV-2025-010', 'pending', 2, '2025-01-15 10:00:00', NULL, NULL, NULL, NULL, 32.5612, -116.9845, NULL, NULL, NULL, NULL, NULL),
(3, 3, 11, 'INV-2025-011', 'pending', 3, '2025-01-15 11:15:00', NULL, NULL, NULL, NULL, 32.5567, -116.9798, NULL, NULL, NULL, NULL, NULL),

-- Entregas para FEC 20250116 - Ana Lopez (Playas)
(4, 4, 12, 'INV-2025-012', 'pending', 1, '2025-01-16 08:00:00', NULL, NULL, NULL, NULL, 32.5678, -117.1234, NULL, NULL, NULL, NULL, NULL),
(4, 4, 13, 'INV-2025-013', 'pending', 2, '2025-01-16 09:30:00', NULL, NULL, NULL, NULL, 32.5656, -117.1267, NULL, NULL, NULL, NULL, NULL),
(4, 4, 14, 'INV-2025-014', 'pending', 3, '2025-01-16 11:00:00', NULL, NULL, NULL, NULL, 32.5689, -117.1201, NULL, NULL, NULL, NULL, NULL),

-- Entregas para FEC 20250116 - Pedro Sanchez (La Mesa)
(5, 5, 15, 'INV-2025-015', 'pending', 1, '2025-01-16 08:30:00', NULL, NULL, NULL, NULL, 32.5234, -116.9876, NULL, NULL, NULL, NULL, NULL),
(5, 5, 16, 'INV-2025-016', 'pending', 2, '2025-01-16 10:00:00', NULL, NULL, NULL, NULL, 32.5267, -116.9845, NULL, NULL, NULL, NULL, NULL);

-- 6. NO INSERTAR TRACKING POINTS
-- Los tracking points se crean automáticamente cuando el conductor inicia/termina entregas
-- Por eso esta tabla queda vacía al inicio

-- 7. MOSTRAR RESUMEN DE DATOS INSERTADOS
PRINT 'Datos básicos ficticios insertados exitosamente para Tijuana:';
SELECT 'Drivers' as Tabla, COUNT(*) as Total FROM drivers
UNION ALL
SELECT 'Salespersons' as Tabla, COUNT(*) as Total FROM salespersons
UNION ALL  
SELECT 'Clients' as Tabla, COUNT(*) as Total FROM clients
UNION ALL
SELECT 'FECs' as Tabla, COUNT(*) as Total FROM fecs
UNION ALL
SELECT 'Deliveries' as Tabla, COUNT(*) as Total FROM deliveries
UNION ALL
SELECT 'Tracking Points' as Tabla, COUNT(*) as Total FROM tracking_points;

-- 8. MOSTRAR ALGUNOS DATOS DE EJEMPLO
PRINT '';
PRINT 'FECs creados (solo datos básicos):';
SELECT 
    f.fec_number, 
    f.fec_date, 
    f.status, 
    d.username as driver_username,
    d.vehicle_plate,
    COUNT(del.delivery_id) as total_deliveries
FROM fecs f
INNER JOIN drivers d ON f.driver_id = d.driver_id
LEFT JOIN deliveries del ON f.fec_id = del.fec_id
GROUP BY f.fec_number, f.fec_date, f.status, d.username, d.vehicle_plate
ORDER BY f.fec_date, f.fec_number;

PRINT '';
PRINT 'Entregas creadas (todas en estado pending, sin datos del sistema):';
SELECT 
    del.invoice_id,
    f.fec_number,
    c.name as client_name,
    del.status,
    del.priority,
    d.username as driver_username,
    CASE 
        WHEN del.delivery_time IS NULL THEN 'Sin completar'
        ELSE 'Completada'
    END as completion_status
FROM deliveries del
INNER JOIN fecs f ON del.fec_id = f.fec_id
INNER JOIN clients c ON del.client_id = c.client_id  
INNER JOIN drivers d ON del.driver_id = d.driver_id
ORDER BY f.fec_number, del.priority;

PRINT '';
PRINT 'Ubicaciones de clientes en Tijuana:';
SELECT TOP 5
    c.name as client_name,
    c.gps_location,
    s.name as salesperson_name,
    CASE 
        WHEN c.gps_location LIKE '32.51%' THEN 'Centro'
        WHEN c.gps_location LIKE '32.53%' THEN 'Zona Río'  
        WHEN c.gps_location LIKE '32.55%' OR c.gps_location LIKE '32.56%' THEN 'Mesa de Otay'
        WHEN c.gps_location LIKE '32.56%,-117.12%' THEN 'Playas'
        WHEN c.gps_location LIKE '32.52%,-116.98%' THEN 'La Mesa'
        ELSE 'Otra Zona'
    END as zona_tijuana
FROM clients c
INNER JOIN salespersons s ON c.salesperson_id = s.salesperson_id
ORDER BY c.client_id;

PRINT '';
PRINT '*** NOTA: ***';
PRINT 'Todos los campos que se llenan automáticamente por el sistema están como NULL:';
PRINT '- delivery_time, accepted_next_at, actual_duration, estimated_duration';
PRINT '- end_latitud, end_longitud, distance';
PRINT '- tracking_points (tabla vacía)';
PRINT '- optimized_order_list_json, suggested_journey_polyline en FECs';
PRINT '';
PRINT 'Estos campos se llenan cuando:';
PRINT '- El conductor inicia una entrega (start_delivery)';
PRINT '- El conductor completa una entrega (end_delivery)';
PRINT '- El sistema optimiza rutas';
PRINT '- Se reportan incidencias';
