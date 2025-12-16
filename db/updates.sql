use Studify_db
GO

ALTER TABLE study_logs 
ADD task_id INT NULL;

ALTER TABLE study_logs 
ADD CONSTRAINT study_logs_task 
FOREIGN KEY (task_id) REFERENCES tasks(task_id);

ALTER TABLE friends 
ADD sent_by_id INT NOT NULL;

ALTER TABLE friends 
ADD CONSTRAINT FK_friends_sender 
FOREIGN KEY (sent_by_id) REFERENCES users(id);
