-- Функция: вычисление ср оценки для студента
CREATE OR REPLACE FUNCTION GetStudentAvgGrade(p_student_id INTEGER)
RETURN NUMBER
IS
    v_avg NUMBER;
BEGIN
    SELECT AVG(dg.name_grade) INTO v_avg
    FROM Grades g
    JOIN DirGrades dg ON g.id_grade = dg.id
    WHERE g.student_id = p_student_id;
    
    RETURN NVL(v_avg, 0);
END GetStudentAvgGrade;
/

SELECT GetStudentAvgGrade(29) FROM dual;




-- ПРОЦЕДУРА: добавление студента с проверкой дубликатов
CREATE OR REPLACE PROCEDURE AddStudent(

    p_i_name IN VARCHAR2,
    p_f_name IN VARCHAR2,  
    p_o_name IN VARCHAR2,  
    p_sex IN VARCHAR2,     
    p_group_id IN INTEGER
)
IS
    -- Секция объявления локальных переменных
    v_exists INTEGER;
BEGIN
    -- COUNT(*) подсчитает количество совпадающих строк
    SELECT COUNT(*) INTO v_exists
    FROM Student
    WHERE i_name = p_i_name 
      AND f_name = p_f_name 
      AND o_name = p_o_name
      AND id_group = p_group_id;
    
    IF v_exists > 0 THEN
        -- Если дубликат найден – вызываем пользовательскую ошибку
        -- -20001 ... -20999 — диапазон пользовательских ошибок Oracle
        RAISE_APPLICATION_ERROR(-20001, 
            'Студент ' || p_i_name || ' ' || p_f_name || ' ' || p_o_name || 
            ' уже существует в группе ' || p_group_id);
    ELSE
        -- Вставка нового студента
        INSERT INTO Student (i_name, f_name, o_name, sex, id_group)
        VALUES (p_i_name, p_f_name, p_o_name, p_sex, p_group_id);
        
        -- Информационное сообщение (видно при SET SERVEROUTPUT ON)
        DBMS_OUTPUT.PUT_LINE('Студент успешно добавлен');
    END IF;
    
    -- Фиксация транзакции (сохраняем изменения)
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        -- Переброс исключения наверх (чтобы вызывающий код знал об ошибке)
        RAISE;
END AddStudent;
/


SET SERVEROUTPUT ON;
BEGIN
    AddStudent('Иванов', 'Иван', 'Иванович', 'М', 1);
END;
/
