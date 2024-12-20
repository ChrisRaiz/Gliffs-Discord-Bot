CREATE TABLE IF NOT EXISTS guilds (
	guild_id BIGINT PRIMARY KEY,
	prefix VARCHAR (5) DEFAULT "!"
);

CREATE TABLE IF NOT EXISTS exp (
	user_id BIGINT PRIMARY KEY,
	xp INTEGER DEFAULT 0,
	level SMALLINT DEFAULT 0,
	xp_Lock TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mutes (
	user_id BIGINT PRIMARY KEY,
	role_ids TEXT,
	end_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS starboard (
	root_message_id BIGINT PRIMARY KEY,
	star_message_id BIGINT UNIQUE,
	stars INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS polls (
	poll_message_id BIGINT PRIMARY KEY,
	poll_channel_id BIGINT NOT NULL,
	question TEXT NOT NULL UNIQUE
);