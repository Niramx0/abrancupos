-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: proyecto_eps
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping events for database 'proyecto_eps'
--

--
-- Dumping routines for database 'proyecto_eps'
--
/*!50003 DROP PROCEDURE IF EXISTS `CambiarEstadoCita` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CambiarEstadoCita`(
    IN p_id_cita INT,
    IN p_nuevo_estado INT,
    IN p_diagnostico TEXT,
    IN p_id_medicamento INT,
    IN p_cantidad_med INT
)
BEGIN
    DECLARE v_count INT;
    DECLARE v_id_usuario INT;

    -- Verificar si la cita existe
    SELECT COUNT(*) INTO v_count FROM citas_medicas WHERE id = p_id_cita;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cita no existe';
    END IF;

    -- Obtener el id_usuario de la cita
    SELECT id_usuario INTO v_id_usuario FROM citas_medicas WHERE id = p_id_cita LIMIT 1;

    -- Verificar si el nuevo estado es válido
    SELECT COUNT(*) INTO v_count FROM estado_cita WHERE id = p_nuevo_estado;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estado no es válido';
    END IF;

    -- Si el estado es "Realizada" (3), el diagnóstico es obligatorio
    IF p_nuevo_estado = 3 AND (p_diagnostico IS NULL OR p_diagnostico = '') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Debe proporcionar un diagnóstico para finalizar la cita';
    END IF;

    -- Actualizar el estado de la cita
    UPDATE citas_medicas 
    SET estado_cita = p_nuevo_estado
    WHERE id = p_id_cita;

    -- Si la cita se marca como "Realizada", insertamos en historial_medico
    IF p_nuevo_estado = 3 THEN
        -- Verificar si el medicamento existe si se proporciona
        IF p_id_medicamento IS NOT NULL THEN
            SELECT COUNT(*) INTO v_count FROM medicamentos WHERE id = p_id_medicamento;
            IF v_count = 0 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El medicamento no existe';
            END IF;

            -- La cantidad de medicamentos debe ser mayor a 0 si se proporciona un medicamento
            IF p_cantidad_med IS NULL OR p_cantidad_med <= 0 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Debe proporcionar una cantidad válida de medicamentos';
            END IF;
        END IF;

        -- Insertar en historial médico
        INSERT INTO historial_medico (id_usuario, id_cita, diagnostico, medicamentos, cantidad_med)
        VALUES (v_id_usuario, p_id_cita, p_diagnostico, p_id_medicamento, p_cantidad_med);
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ConsultarHistorialMedico` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ConsultarHistorialMedico`(
    IN p_id_usuario INT
)
BEGIN
    -- Verificar si el usuario tiene historial médico
    IF NOT EXISTS (SELECT 1 FROM historial_medico WHERE id_usuario = p_id_usuario) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario no tiene historial médico registrado.';
    END IF;

    -- Obtener el historial médico del usuario
    SELECT 
        hm.id_cita,
        c.id_medico,
        m.nombre AS nombre_medico,
        c.fecha AS fecha_cita,
        hm.diagnostico,
        med.nombre AS medicamento,
        hm.cantidad_med AS cantidad_medicamento
    FROM historial_medico hm
    JOIN citas_medicas c ON hm.id_cita = c.id
    JOIN medicos m ON c.id_medico = m.id
    LEFT JOIN medicamentos med ON hm.medicamentos = med.id
    WHERE hm.id_usuario = p_id_usuario
    ORDER BY c.fecha DESC;
    
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `RegistrarCitaMedica` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `RegistrarCitaMedica`(
    IN p_id_usuario INT,
    IN p_id_medico INT,
    IN p_fecha DATE
)
BEGIN
    DECLARE v_count INT;

    SELECT COUNT(*) INTO v_count FROM paciente WHERE id = p_id_usuario;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario no existe';
    END IF;

    SELECT COUNT(*) INTO v_count FROM medicos WHERE id = p_id_medico;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El médico no existe';
    END IF;

    SELECT COUNT(*) INTO v_count FROM citas_medicas 
    WHERE id_usuario = p_id_usuario AND id_medico = p_id_medico AND fecha = p_fecha;
    
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario ya tiene una cita con este médico en la misma fecha';
    END IF;

    INSERT INTO citas_medicas (id_usuario, id_medico, fecha, estado_cita)
    VALUES (p_id_usuario, p_id_medico, p_fecha, 1);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ReservarMedicamento` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ReservarMedicamento`(
    IN p_id_cita INT
)
BEGIN
    DECLARE v_id_medicamento INT;
    DECLARE v_cantidad INT;
    DECLARE v_stock_actual INT;
    DECLARE v_precio_unitario DECIMAL(10,2);
    DECLARE v_precio_total DECIMAL(10,2);

    -- Obtener el medicamento y cantidad desde historial_medico
    SELECT medicamentos, cantidad_med 
    INTO v_id_medicamento, v_cantidad
    FROM historial_medico
    WHERE id_cita = p_id_cita;

    -- Verificar si la cita existe en historial_medico
    IF v_id_medicamento IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'La cita no tiene medicamentos asignados en el historial médico.';
    END IF;

    -- Verificar que el medicamento existe en la tabla medicamentos
    IF NOT EXISTS (SELECT 1 FROM medicamentos WHERE id = v_id_medicamento) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'El medicamento no existe en la base de datos.';
    END IF;

    -- Obtener stock actual y precio unitario del medicamento
    SELECT stock, precio INTO v_stock_actual, v_precio_unitario 
    FROM medicamentos 
    WHERE id = v_id_medicamento;

    -- Verificar si hay stock suficiente
    IF v_stock_actual < v_cantidad THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Stock insuficiente para el medicamento solicitado.';
    END IF;

    -- Calcular el precio total
    SET v_precio_total = v_precio_unitario * v_cantidad;

    -- Descontar stock del medicamento
    UPDATE medicamentos
    SET stock = stock - v_cantidad
    WHERE id = v_id_medicamento;

    -- Confirmación con precio total
    SELECT 
        CONCAT('Se han reservado ', v_cantidad, ' unidades del medicamento. Por favor hacer el pago y reclamación en nuestra sede central') AS Reserva,
        v_precio_total AS Precio;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-06 21:33:41
