-- Magnolia Royale: gerado a partir das Models. Use em uma base vazia.

CREATE DATABASE IF NOT EXISTS magnolia_royale CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE magnolia_royale;

CREATE TABLE contatos (
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(180) NOT NULL, 
	subject VARCHAR(180) NOT NULL, 
	message TEXT NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id)
);

CREATE TABLE usuarios (
	email VARCHAR(180) NOT NULL, 
	`displayName` VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	`role` VARCHAR(20) NOT NULL, 
	`photoURL` VARCHAR(500), 
	phone VARCHAR(25), 
	`emailVerified` BOOL NOT NULL, 
	active BOOL NOT NULL, 
	session_version INTEGER NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	preferences JSON NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE arquivos (
	`ownerId` INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	`originalName` VARCHAR(255) NOT NULL, 
	`mimeType` VARCHAR(80) NOT NULL, 
	private BOOL NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`ownerId`) REFERENCES usuarios (id), 
	UNIQUE (name)
);

CREATE TABLE buscas (
	`userId` INTEGER NOT NULL, 
	term VARCHAR(180) NOT NULL, 
	filters JSON NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`userId`) REFERENCES usuarios (id)
);

CREATE TABLE clinicas (
	`ownerId` INTEGER NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	cnpj VARCHAR(14) NOT NULL, 
	email VARCHAR(180) NOT NULL, 
	phone VARCHAR(25) NOT NULL, 
	street VARCHAR(180) NOT NULL, 
	number VARCHAR(20) NOT NULL, 
	city VARCHAR(100) NOT NULL, 
	state VARCHAR(2) NOT NULL, 
	`zipCode` VARCHAR(12) NOT NULL, 
	neighborhood VARCHAR(100) NOT NULL, 
	description TEXT NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	verified BOOL NOT NULL, 
	rating NUMERIC(3, 1) NOT NULL, 
	`reviewCount` INTEGER NOT NULL, 
	score INTEGER NOT NULL, 
	plan VARCHAR(20) NOT NULL, 
	images JSON NOT NULL, 
	`cancellationPolicy` JSON NOT NULL, 
	`adminFeedback` TEXT, 
	`assessmentCompleted` BOOL NOT NULL, 
	`verificationCriteria` JSON, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`ownerId`), 
	FOREIGN KEY(`ownerId`) REFERENCES usuarios (id), 
	UNIQUE (cnpj)
);

CREATE TABLE notificacoes (
	`userId` INTEGER NOT NULL, 
	type VARCHAR(30) NOT NULL, 
	title VARCHAR(180) NOT NULL, 
	message TEXT NOT NULL, 
	link VARCHAR(250), 
	`read` BOOL NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`userId`) REFERENCES usuarios (id)
);

CREATE TABLE tokens_conta (
	`userId` INTEGER NOT NULL, 
	token_hash VARCHAR(64) NOT NULL, 
	purpose VARCHAR(20) NOT NULL, 
	`expiresAt` DATETIME NOT NULL, 
	used BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`userId`) REFERENCES usuarios (id), 
	UNIQUE (token_hash)
);

CREATE TABLE agendas (
	`clinicId` INTEGER NOT NULL, 
	`daysOfWeek` JSON NOT NULL, 
	`startTime` VARCHAR(5) NOT NULL, 
	`endTime` VARCHAR(5) NOT NULL, 
	`slotDuration` INTEGER NOT NULL, 
	`blockedDates` JSON NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`clinicId`), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE checkouts_demonstracao (
	`clinicId` INTEGER NOT NULL, 
	plan VARCHAR(20) NOT NULL, 
	price NUMERIC(10, 2) NOT NULL, 
	`paymentMethod` VARCHAR(20), 
	status VARCHAR(20) NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	`paidAt` DATETIME, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE conversas (
	`clientId` INTEGER NOT NULL, 
	`clinicId` INTEGER, 
	kind VARCHAR(15) NOT NULL, 
	`clientName` VARCHAR(120) NOT NULL, 
	`clinicName` VARCHAR(160), 
	`lastMessage` TEXT, 
	`lastMessageAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`clientId`, `clinicId`, kind), 
	FOREIGN KEY(`clientId`) REFERENCES usuarios (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE denuncias (
	`clinicId` INTEGER NOT NULL, 
	`reporterId` INTEGER NOT NULL, 
	reason VARCHAR(150) NOT NULL, 
	description TEXT NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id), 
	FOREIGN KEY(`reporterId`) REFERENCES usuarios (id)
);

CREATE TABLE favoritos (
	`userId` INTEGER NOT NULL, 
	`clinicId` INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`userId`, `clinicId`), 
	FOREIGN KEY(`userId`) REFERENCES usuarios (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE procedimentos (
	`clinicId` INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	price NUMERIC(10, 2) NOT NULL, 
	active BOOL NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`clinicId`, name), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE profissionais (
	uid INTEGER NOT NULL, 
	`clinicId` INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(180) NOT NULL, 
	bio TEXT NOT NULL, 
	`photoURL` VARCHAR(500), 
	active BOOL NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (uid), 
	FOREIGN KEY(uid) REFERENCES usuarios (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE publicacoes (
	`clinicId` INTEGER NOT NULL, 
	title VARCHAR(180) NOT NULL, 
	excerpt VARCHAR(500) NOT NULL, 
	content TEXT NOT NULL, 
	image VARCHAR(500), 
	author VARCHAR(120) NOT NULL, 
	category VARCHAR(80), 
	`readTime` INTEGER NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE questionarios (
	`clinicId` INTEGER NOT NULL, 
	answers JSON NOT NULL, 
	`updatedAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`clinicId`), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id)
);

CREATE TABLE agendamentos (
	`clinicId` INTEGER NOT NULL, 
	`professionalId` INTEGER NOT NULL, 
	`clientId` INTEGER NOT NULL, 
	`procedureId` INTEGER NOT NULL, 
	`clientName` VARCHAR(120) NOT NULL, 
	`professionalName` VARCHAR(120) NOT NULL, 
	`procedure` VARCHAR(120) NOT NULL, 
	date DATE NOT NULL, 
	time VARCHAR(5) NOT NULL, 
	duration INTEGER NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	valor NUMERIC(10, 2) NOT NULL, 
	notes TEXT, 
	`cancelReason` TEXT, 
	`cancellationFee` NUMERIC(10, 2) NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id), 
	FOREIGN KEY(`professionalId`) REFERENCES profissionais (id), 
	FOREIGN KEY(`clientId`) REFERENCES usuarios (id), 
	FOREIGN KEY(`procedureId`) REFERENCES procedimentos (id)
);

CREATE INDEX ix_agenda_profissional ON agendamentos (`professionalId`, date, status);

CREATE TABLE mensagens (
	`chatId` INTEGER NOT NULL, 
	`senderId` INTEGER NOT NULL, 
	`senderName` VARCHAR(120) NOT NULL, 
	text TEXT NOT NULL, 
	`read` BOOL NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`chatId`) REFERENCES conversas (id), 
	FOREIGN KEY(`senderId`) REFERENCES usuarios (id)
);

CREATE TABLE portfolio (
	`professionalId` INTEGER NOT NULL, 
	`imageUrl` VARCHAR(500) NOT NULL, 
	`procedure` VARCHAR(120) NOT NULL, 
	description TEXT, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`professionalId`) REFERENCES profissionais (id)
);

CREATE TABLE profissional_procedimentos (
	`professionalId` INTEGER NOT NULL, 
	`procedureId` INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`professionalId`, `procedureId`), 
	FOREIGN KEY(`professionalId`) REFERENCES profissionais (id), 
	FOREIGN KEY(`procedureId`) REFERENCES procedimentos (id)
);

CREATE TABLE avaliacoes (
	`clinicId` INTEGER NOT NULL, 
	`clientId` INTEGER NOT NULL, 
	`professionalId` INTEGER, 
	`appointmentId` INTEGER NOT NULL, 
	`clientName` VARCHAR(120) NOT NULL, 
	rating INTEGER NOT NULL, 
	comment TEXT NOT NULL, 
	images JSON NOT NULL, 
	helpful INTEGER NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	UNIQUE (`clinicId`, `clientId`), 
	CHECK (rating BETWEEN 1 AND 5), 
	FOREIGN KEY(`clinicId`) REFERENCES clinicas (id), 
	FOREIGN KEY(`clientId`) REFERENCES usuarios (id), 
	FOREIGN KEY(`professionalId`) REFERENCES profissionais (id), 
	FOREIGN KEY(`appointmentId`) REFERENCES agendamentos (id)
);

CREATE TABLE historico_agendamentos (
	`appointmentId` INTEGER NOT NULL, 
	`actorId` INTEGER NOT NULL, 
	action VARCHAR(30) NOT NULL, 
	details JSON NOT NULL, 
	`createdAt` DATETIME NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(`appointmentId`) REFERENCES agendamentos (id), 
	FOREIGN KEY(`actorId`) REFERENCES usuarios (id)
);
