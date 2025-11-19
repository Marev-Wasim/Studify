use Studify_db
GO

ALTER TABLE study_logs 
ADD task_id INT NULL;

ALTER TABLE study_logs 
ADD CONSTRAINT study_logs_task 
    FOREIGN KEY (task_id) REFERENCES tasks(task_id);

