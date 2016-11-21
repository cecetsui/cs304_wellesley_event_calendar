use eventscal_db;
drop table if exists orgs_contacts;
drop table if exists orgs_events;
drop table if exists head_contacts;
drop table if exists orgs;
drop table if exists events;


CREATE TABLE events (
	event_id INT AUTO_INCREMENT PRIMARY KEY,
	spam VARCHAR(100),
	name VARCHAR(50) not null,
	event_date DATE not null,
	time_start TIME not null,
	time_end TIME not null,
	description VARCHAR(500) not null,
	location VARCHAR(25) not null,
	event_type ENUM('Lecture', 'Meeting', 'Performance', 'Rehearsal', 'Workshop', 'Conference', 'Exhibit', 'Film Showing', 'Panel', 'Party', 'Recital', 'Seminar', 'Reception', 'Community Service', 'Other')
) ENGINE = INNODB;
	

CREATE TABLE orgs (
	org_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) not null,
	description VARCHAR(500) not null,
	email VARCHAR(25),
	website VARCHAR(200),
	org_type ENUM('Academic' , 'Career', 'CGHP Affiliates', 'Cultural', 'Media & Publication', 'Performance & Arts', 'Political', 'Religious', 'Social Justice & Awareness', 'Societies', 'Sports & Teams', 'Volunteer')
) ENGINE = INNODB;


CREATE TABLE head_contacts (
	bnumber INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) not null,
	email VARCHAR(25) not null,
	location VARCHAR(25) not null,
	contact_type ENUM('Student', 'Staff')
) ENGINE = INNODB;


CREATE TABLE orgs_events (
	org_id INT not null,
	event_id INT not null,
	PRIMARY KEY (org_id, event_id),
	FOREIGN KEY (org_id)
		REFERENCES orgs(org_id)
		ON UPDATE cascade ON DELETE restrict,
	FOREIGN KEY (event_id)
		REFERENCES events(event_id)
		ON UPDATE cascade ON DELETE restrict
) ENGINE = INNODB;


CREATE TABLE orgs_contacts (
	org_id INT not null,
	bnumber INT not null,
	date_added DATE not null,
	PRIMARY KEY (org_id, bnumber, date_added),
	FOREIGN KEY (org_id)
		REFERENCES orgs(org_id)
		ON UPDATE cascade ON DELETE restrict,
	FOREIGN KEY (bnumber)
		REFERENCES head_contacts(bnumber)
		ON UPDATE cascade ON DELETE restrict
) ENGINE = INNODB;


