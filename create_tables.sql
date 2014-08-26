CREATE TABLE Game(
    GameID                  smallint       auto_increment, 
    Genre                   varchar(50),
    Review                  text,
    StarRating              smallint,
    ClassificationRating    varchar(5),
    PlatformNotes           text,
    PromotionLink           varchar(50),
    Cost                    decimal(5,2),      
    PRIMARY KEY(GameID)
) ENGINE=InnoDB;
    
CREATE TABLE Video (
    VideoID         smallint       auto_increment,
    URL             varchar(50)    NOT_NULL,
    Price           decimal(5,2),
    VideoType       varchar(45),
    InstanceRunID   smallint       NOT_NULL,
    GameID          smallint       NOT_NULL,
    PRIMARY KEY(AccountID),
    FOREIGN KEY (InstanceRunID) REFERENCES (InstanceRun)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (GameID) REFERENCES (Game)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE InstanceRun (
    InstanceRunID         smallint       auto_increment,
    SupervisorID          smallint       NOT_NULL,
    Name                  varchar(45),
    RecordedTime          DATETIME,
    CategoryName          varchar(50),
    PRIMARY KEY(InstanceRunID),
    FOREIGN KEY (SupervisorID) REFERENCES (Player)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Achievement (
    AchievementID         smallint       auto_increment,
    InstanceRunID         smallint       NOT_NULL,
    WhenAchieved          DATETIME
    Name                  varchar(45),
    RewardBody            varchar(45),
    PRIMARY KEY(AchievementID, InstanceRunID),
    FOREIGN KEY (InstanceRunID) REFERENCES (InstanceRun)
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



