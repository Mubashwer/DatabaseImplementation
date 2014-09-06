CREATE TABLE Game(
    GameID                  MEDIUMINT      AUTO_INCREMENT,  #it is possible to play more than 32k games in the long run
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
    VideoID                 MEDIUMINT      AUTO_INCREMENT, #many videos at every instance run
    URL                     VARCHAR(50)    NOT NULL,
    Price                   DECIMAL(5,2),
    VideoType               VARCHAR(45),
    InstanceRunID           SMALLINT       NOT NULL,
    GameID                  MEDIUMINT      NOT NULL, #changed to match
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


) ENGINE=InnoDB;


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

) ENGINE=InnoDB;

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
	) ENGINE=InnoDB;

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
) ENGINE=InnoDB;

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

CREATE TABLE Viewer(
    ViewerID INT UNSIGNED AUTO_INCREMENT,
    /*MODIFIED from smallint, we're hoping for a lot of viewers! */
    ViewerType VARCHAR(45) NOT NULL, 
    /* Possible values n for none/normal, C for CrowdFunding, P for 
    Premium and B for Both */
    DateOfBirth  DATE,
    Email        VARCHAR(50),
    PRIMARY KEY   (ViewerID)
)ENGINE=InnoDB;

CREATE TABLE CrowdFundingViewer(
    ViewerID INT UNSIGNED,
    /* MODIFIED to match */
    FirstName           VARCHAR(45),
    LastName            VARCHAR(45),
    TotalAmountDonated  DECIMAL(9,2),
    /* MODIFIED from VARCHAR(45).  Allows for donations to sum to 
    $9,999,999.99 (to be safe).  Do we think less?*/
    PRIMARY KEY (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
        /* I currently have no idea what these mean */
)ENGINE=InnoDB;

CREATE TABLE PremiumViewer(
    ViewerID INT UNSIGNED,
    /* MODIFIED to match */
    RenewalDate DATE NOT NULL,
    PRIMARY KEY  (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)ENGINE=InnoDB;

CREATE TABLE ViewerOrder(
    ViewerOrderID INT AUTO_INCREMENT,
    /* MODIFIED from smallint to unsigned int, allowing for up to
    ~4 billion orders to be made */
    OrderDate     DATE      NOT  NULL,
    ViewedStatus  CHAR(7)   NOT  NULL,
    ViewerID      INT UNSIGNED  NOT    NULL,
    /* MODIFIED to match */
    PRIMARY KEY (ViewerOrderID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)ENGINE=InnoDB;

CREATE TABLE ViewerOrderLine(
    VideoID        MEDIUMINT, #mubashwer: changed to match mine
    ViewerOrderID  SMALLINT,
    FlagPerk       BOOLEAN    NOT  NULL,
    PRIMARY KEY (VideoID,ViewerOrderID),
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (ViewerOrderID) REFERENCES ViewerOrder(ViewerOrderID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
)ENGINE=InnoDB;


