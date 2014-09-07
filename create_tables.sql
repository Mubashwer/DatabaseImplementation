DROP TABLE IF EXISTS PlayerAddress;
DROP TABLE IF EXISTS ViewerAddress;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS ViewerOrderLine;
DROP TABLE IF EXISTS ViewerOrder;
DROP TABLE IF EXISTS PremiumViewer;
DROP TABLE IF EXISTS CrowdFundingViewer;
DROP TABLE IF EXISTS Viewer;
DROP TABLE IF EXISTS VenueEquipment;
DROP TABLE IF EXISTS Equipment;
DROP TABLE IF EXISTS Venue;
DROP TABLE IF EXISTS Video;
DROP TABLE IF EXISTS Achievement;
DROP TABLE IF EXISTS InstanceRun;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Game;

#Mubashwer
CREATE TABLE Game(
    GameID                  MEDIUMINT      AUTO_INCREMENT,  #it is possible to play more than 32k games in the long run
    Genre                   VARCHAR(50)    DEFAULT NULL,
    Review                  TEXT           DEFAULT NULL,
    StarRating              SMALLINT       DEFAULT NULL,
    ClassificationRating    VARCHAR(5)     DEFAULT NULL,
    PlatformNotes           TEXT           DEFAULT NULL,
    PromotionLink           VARCHAR(50)    DEFAULT NULL,
    Cost                    DECIMAL(5,2)   DEFAULT NULL,   
    PRIMARY KEY (GameID)
) ENGINE=InnoDB;

#Kendra
CREATE TABLE Player (
    PlayerID                SMALLINT       AUTO_INCREMENT,
    SupervisorID            SMALLINT       DEFAULT NULL, # supervisor is optional
    FirstName               VARCHAR(50)    NOT NULL,
    LastName                VARCHAR(50)    NOT NULL,
    Role                    VARCHAR(50)    NOT NULL,
    PlayerType              VARCHAR(1)     NOT NULL, #Type is a keyword
    ProfileDescription      TEXT           DEFAULT NULL,          
    Email                   VARCHAR(50)    NOT NULL,
    GameHandle              VARCHAR(12)    NOT NULL,
    Phone                   VARCHAR(14)    DEFAULT NULL,
    VoiP                    VARCHAR(30)    NOT NULL,
    PRIMARY KEY (PlayerID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID) 
	    ON DELETE RESTRICT
	    ON UPDATE CASCADE
) ENGINE=InnoDB;

#Mubashwer    
CREATE TABLE InstanceRun (
    InstanceRunID           SMALLINT       AUTO_INCREMENT,
    SupervisorID            SMALLINT       NOT NULL,
    InstanceName            VARCHAR(45)    DEFAULT NULL,   # changed name from Name (as Name is part of syntax)
    RecordedTime            DATETIME       DEFAULT NULL,
    CategoryName            VARCHAR(50)    DEFAULT NULL,
    PRIMARY KEY (InstanceRunID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Mubashwer
CREATE TABLE Achievement (
    AchievementID           SMALLINT       AUTO_INCREMENT,
    InstanceRunID           SMALLINT       NOT NULL,
    WhenAchieved            DATETIME       DEFAULT NULL,
    AchievementName         VARCHAR(45)    DEFAULT NULL, # changed name from Name (as Name is part of syntax)
    RewardBody              VARCHAR(45)    DEFAULT NULL,
    PRIMARY KEY (AchievementID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Mubashwer
CREATE TABLE Video (
    VideoID                 MEDIUMINT      AUTO_INCREMENT, #many videos at every instance run
    URL                     VARCHAR(50)    NOT NULL,
    Price                   DECIMAL(5,2)   DEFAULT 0.00,
    VideoType               VARCHAR(45)    DEFAULT NULL,
    InstanceRunID           SMALLINT       NOT NULL,
    GameID                  MEDIUMINT      NOT NULL, #changed to match
    PRIMARY KEY (VideoID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Kendra
CREATE TABLE Venue (
    VenueID                 SMALLINT       AUTO_INCREMENT,
    VenueName               VARCHAR(50)    NOT NULL, #Name is a keyword
    VenueDescription        TEXT           DEFAULT NULL,
    PowerOutlets            SMALLINT       DEFAULT NULL,
    LightingNotes           TEXT           DEFAULT NULL,
    SupervisorID            SMALLINT       NOT NULL,
    PRIMARY KEY (VenueID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID)
	    ON DELETE RESTRICT
	    ON UPDATE CASCADE
) ENGINE=InnoDB;

#Kendra
CREATE TABLE Equipment (
    EquipmentID             SMALLINT       AUTO_INCREMENT,
    ModelAndMake            VARCHAR(45)    DEFAULT NULL,
    EquipmentReview         TEXT           DEFAULT NULL,
    ProcessorSpeed          VARCHAR(45)    DEFAULT NULL,
    PRIMARY KEY (EquipmentID)
) ENGINE=InnoDB;

#Kendra
CREATE TABLE VenueEquipment (
    VenueID                 SMALLINT       NOT NULL,
    EquipmentID             SMALLINT       NOT NULL,
    FinancialYearStartingDate   DATE       NOT NULL,
    SoftwareVersion         VARCHAR(45)    DEFAULT NULL,
    PRIMARY KEY (VenueID, EquipmentID),
    FOREIGN KEY (VenueID) REFERENCES Venue(VenueID)
	    ON DELETE RESTRICT
	    ON UPDATE CASCADE,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
	    ON DELETE RESTRICT
	    ON UPDATE CASCADE
) ENGINE=InnoDB;

#Jaye
CREATE TABLE Viewer(
    ViewerID                INT UNSIGNED   AUTO_INCREMENT,
    /*MODIFIED from smallint, we're hoping for a lot of viewers! */
    FirstName               VARCHAR(45)    DEFAULT NULL,
    LastName                VARCHAR(45)    DEFAULT NULL,    
    ViewerType              CHAR(1)        DEFAULT "N" NOT NULL, #changed to char(1)
    /* Possible values N for none/normal, C for CrowdFunding, P for 
    Premium and B for Both */
    DateOfBirth             DATE           DEFAULT NULL,
    Email                   VARCHAR(50)    DEFAULT NULL,
    PRIMARY KEY (ViewerID)
) ENGINE=InnoDB;

#Jaye
CREATE TABLE CrowdFundingViewer(
    ViewerID                INT UNSIGNED   NOT NULL,
    TotalAmountDonated      DECIMAL(9,2)   DEFAULT 0.00,
    /* MODIFIED from VARCHAR(45).  Allows for donations to sum to 
    $9,999,999.99 (to be safe).  Do we think less?*/
    PRIMARY KEY (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
        /* I currently have no idea what these mean */
) ENGINE=InnoDB;

#Jaye
CREATE TABLE PremiumViewer(
    ViewerID                INT UNSIGNED   NOT NULL,
    /* MODIFIED to match */
    RenewalDate             DATE           NOT NULL,
    PRIMARY KEY (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Jaye
CREATE TABLE ViewerOrder(
    ViewerOrderID           INT UNSIGNED   AUTO_INCREMENT,
    /* MODIFIED from smallint to unsigned int, allowing for up to
    ~4 billion orders to be made */
    OrderDate               DATE           NOT NULL,
    ViewedStatus            CHAR(7)        NOT NULL,
    ViewerID                INT UNSIGNED   NOT NULL,
    /* MODIFIED to match */
    PRIMARY KEY (ViewerOrderID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Jaye
CREATE TABLE ViewerOrderLine(
    VideoID                 MEDIUMINT      NOT NULL, #changed to match
    ViewerOrderID           INT UNSIGNED   NOT NULL,
    FlagPerk                BOOLEAN        NOT NULL,
    PRIMARY KEY (VideoID, ViewerOrderID),
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (ViewerOrderID) REFERENCES ViewerOrder(ViewerOrderID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Geordie
CREATE TABLE Address(
    AddressID               SMALLINT       AUTO_INCREMENT,
    StreetNumber            SMALLINT       NOT NULL,
    StreetNumberSuffix      VARCHAR(20)    DEFAULT NULL,
    StreetName              VARCHAR(50)    NOT NULL,
    StreetType              VARCHAR(20)    NOT NULL,
    AddressType             VARCHAR(20)    DEFAULT NULL,
    AddressTypeIdentifier   VARCHAR(20)    DEFAULT NULL,
    MinorMunicipality       VARCHAR(50)    DEFAULT NULL,
    MajorMunicipality       VARCHAR(50)    NOT NULL,
    GoverningDistrict       VARCHAR(50)    NOT NULL,
    PostalArea              VARCHAR(10)    NOT NULL, #changed to 10 as in lecture slide
    Country                 VARCHAR(50)    NOT NULL,
   PRIMARY KEY (AddressID)
) ENGINE=InnoDB;

#Geordie
CREATE TABLE ViewerAddress(
    ViewerID               INT UNSIGNED     NOT NULL,
    AddressID              SMALLINT         NOT NULL,
    StartDate              DATE             NOT NULL,
    EndDate                DATE             DEFAULT NULL,
    PRIMARY KEY (ViewerID, AddressID, StartDate),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
	FOREIGN KEY (AddressID) REFERENCES Address(AddressID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

#Geordie
CREATE TABLE PlayerAddress(
    PlayerID               SMALLINT         NOT NULL,
    AddressID              SMALLINT         NOT NULL,
    StartDate              DATE             NOT NULL,
    EndDate                DATE             DEFAULT NULL,			
    PRIMARY KEY (PlayerID, AddressID, StartDate),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
	FOREIGN KEY (AddressID) REFERENCES Address(AddressID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;
