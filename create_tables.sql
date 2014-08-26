CREATE TABLE Game(
    GameID                  SMALLINT       AUTO_INCREMENT, 
    Genre                   VARCHAR(50),
    Review                  TEXT,
    StarRating              SMALLINT,
    ClassificationRating    VARCHAR(5),
    PlatformNotes           TEXT,
    PromotionLink           VARCHAR(50),
    Cost                    DECIMAL(5,2),      
    PRIMARY KEY(GameID)
) ENGINE=InnoDB;
    
CREATE TABLE InstanceRun (
    InstanceRunID           SMALLINT       AUTO_INCREMENT,
    SupervisorID            SMALLINT       NOT NULL,
    InstanceName            VARCHAR(45),   # changed name from Name (as Name is part of syntax)
    RecordedTime            DATETIME,
    CategoryName            VARCHAR(50),
    PRIMARY KEY(InstanceRunID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(SupervisorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Achievement (
    AchievementID           SMALLINT       AUTO_INCREMENT,
    InstanceRunID           SMALLINT       NOT NULL,
    WhenAchieved            DATETIME,
    AchievementName         VARCHAR(45),   # changed name from Name (as Name is part of syntax)
    RewardBody              VARCHAR(45),
    PRIMARY KEY(AchievementID, InstanceRunID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Video (
    VideoID                 SMALLINT       AUTO_INCREMENT,
    URL                     VARCHAR(50)    NOT NULL,
    Price                   DECIMAL(5,2),
    VideoType               VARCHAR(45),
    InstanceRunID           SMALLINT       NOT NULL,
    GameID                  SMALLINT       NOT NULL,
    PRIMARY KEY(VideoID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Viewer(

	ViewerID				SMALLINT		auto_increment,
	ViewerType				CHAR(1)			NOT NULL,
	DateOfBirth 			DATE 			,
	Email					VARCHAR(50)		,
	
	PRIMARY KEY(ViewerID)


)


CREATE TABLE ViewerAddress(

	ViewerID				SMALLINT		NOT NULL,
	AddressID				SMALLINT 		NOT NULL,
	StartDate				DATE 			??????,
	EndDate					DATE 			,

	PRIMARY KEY(StartDate)
	FOREIGN KEY(ViewerID)			REFERENCES Viewer(ViewerID)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	FOREIGN KEY(AddressID)			REFERENCES Address(AddressID)
		ON DELETE RESTRICT
		ON UPDATE CASCADE

)

CREATE TABLE PlayerAddress(

	PlayerID				SMALLINT		NOT NULL,
	AddressID 				SMALLINT 		NOT NULL,
	StartDate 				DATE 			??????,
	EndDate 				DATE 			,

	PRIMARY KEY(StartDate)
	FOREIGN KEY(AddressID)			REFERENCES Address(AddressID)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY(PlayerID)			REFERENCES Player(PlayerID)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
	)

CREATE TABLE Address(

	AddressID				SMALLINT		auto_increment,
	StreetNumber			SMALLINT 		NOT NULL,
	StreetNumberSuffix		VARCHAR(20)		,
	StreetName				VARCHAR(50)		NOT NULL,
	StreetType				VARCHAR(20)		NOT NULL,
	AddressType 			VARCHAR(20)		,
	AddressTypeIdentifier	VARCHAR(20)		,
	MinorMunicipality		VARCHAR(50)		,
	MajorMunicipality		VARCHAR(50)		NOT NULL,
	GoverningDistrict		VARCHAR(50)		NOT NULL,
	PostalArea				VARCHAR(4)		NOT NULL, ? varchar 4???? No US players???
	Country					VARCHAR(50)		NOT NULL,

	PRIMARY KEY(AddressID)
)

CREATE TABLE Player (
PlayerID SMALLINT AUTO_INCREMENT,
SupervisorID SMALLINT AUTO_INCREMENT,
FirstName VARCHAR(50) NOT NULL,
LastName VARCHAR(50) NOT NULL,
Role VARCHAR(50) NOT NULL,
TypeO VARCHAR(1) NOT NULL,
ProfileDescription TEXT,
Email VARCHAR(50) NOT NULL,
GameHandle VARCHAR(50) NOT NULL,
Phone VARCHAR(14),
VoP VARCHAR(30) NOT NULL,
PRIMARY KEY (PlayerID),
PRIMARY KEY (SupervisorID),
FOREIGN KEY (SupervisorID) REFERENCES Player (SupervisorID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
)ENGINE=InnoDB;

CREATE TABLE Venue (
VenueID SMALLINT NOT NULL,
Name VARCHAR(50) NOT NULL,
VenueDescription TEXT,
PowerOutlets SMALLINT,
LightingNotes TEXT,
SupervisorID SMALLINT NOT NULL,
PRIMARY KEY (VenueID),
FOREIGN KEY (SupervisorID) REFERENCES Player (SupervisorID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
)ENGINE=InnoDB;

CREATE TABLE Equipment (
EquipmentID SMALLINT NOt NULL,
ModelAndMake VARCHAR(45),
EquipmentReview TEXT,
ProcessorSpeed VARCHAR(45),
PRIMARY KEY (EquipmentID)
)ENGINE=InnoDB;

CREATE TABLE VenueEquipment (
VenueID SMALLINT NOT NULL,
EquipmentID SMALLINT NOT NULL,
FinancialYearStartingDate DATE NOT NULL,
SoftwareVersion VARCHAR(45),
PRIMARY KEY (VenueID),
PRIMARY KEY (EquipmentID),
FOREIGN KEY (VenueID) REFERENCES Venue (VenueID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE,
FOREIGN KEY (EquipmentID) REFERENCES Equipment (EquipmentID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
)ENGINE=InnoDB;



