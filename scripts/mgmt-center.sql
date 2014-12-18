-- create table environment
CREATE TABLE `environment` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `date` DATETIME NOT NULL,
    `room_id` SMALLINT NOT NULL,
    `temperature` FLOAT NOT NULL,
    `humidity` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci';