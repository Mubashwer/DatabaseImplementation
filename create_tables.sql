DROP TABLE IF EXISTS AccessCodeVideo;
DROP TABLE IF EXISTS AccessCode;
DROP TABLE IF EXISTS InstancePlayer;
DROP TABLE IF EXISTS InstanceEquipment;
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


CREATE TABLE Game(
    GameID                  MEDIUMINT      AUTO_INCREMENT,
    Genre                   VARCHAR(50)    DEFAULT NULL,
    Review                  TEXT           DEFAULT NULL,
    StarRating              SMALLINT       DEFAULT NULL,
    ClassificationRating    VARCHAR(5)     DEFAULT NULL,
    PlatformNotes           TEXT           DEFAULT NULL,
    PromotionLink           VARCHAR(50)    DEFAULT NULL,
    Cost                    DECIMAL(5,2)   DEFAULT NULL,
    GameName                VARCHAR(85)    NOT NULL,
    PRIMARY KEY (GameID)
) ENGINE=InnoDB;


CREATE TABLE Player (
    PlayerID                SMALLINT       AUTO_INCREMENT,
    SupervisorID            SMALLINT       DEFAULT NULL, 
    FirstName               VARCHAR(50)    NOT NULL,
    LastName                VARCHAR(50)    NOT NULL,
    Role                    VARCHAR(50)    NOT NULL,
    PlayerType              CHAR(1)        NOT NULL, 
    ProfileDescription      TEXT           DEFAULT NULL,          
    Email                   VARCHAR(50)    NOT NULL,
    UserName                VARCHAR(12)    NOT NULL,
    HashedPassword          CHAR(128)      NOT NULL,
    Salt                    CHAR(32)       NOT NULL,
    Phone                   VARCHAR(14)    DEFAULT NULL,
    VoiP                    VARCHAR(30)    NOT NULL,
    PRIMARY KEY (PlayerID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID) 
	    ON DELETE SET NULL
	    ON UPDATE CASCADE
) ENGINE=InnoDB;

   
CREATE TABLE InstanceRun (
    InstanceRunID           SMALLINT       AUTO_INCREMENT,
    SupervisorID            SMALLINT       NOT NULL,
    InstanceName            VARCHAR(45)    DEFAULT NULL,  
    RecordedTime            DATETIME       DEFAULT NULL,
    CategoryName            VARCHAR(50)    DEFAULT NULL,
    PRIMARY KEY (InstanceRunID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Achievement (
    AchievementID           SMALLINT       AUTO_INCREMENT,
    InstanceRunID           SMALLINT       NOT NULL,
    WhenAchieved            DATETIME       DEFAULT NULL,
    AchievementName         VARCHAR(45)    DEFAULT NULL,
    RewardBody              VARCHAR(45)    DEFAULT NULL,
    PRIMARY KEY (AchievementID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Video (
    VideoID                 MEDIUMINT      AUTO_INCREMENT, 
    VideoName               VARCHAR(50)    NOT NULL,
    URL                     VARCHAR(50)    NOT NULL,
    Price                   DECIMAL(5,2)   DEFAULT 0.00,
    VideoType               VARCHAR(45)    DEFAULT 'Non-Premium',
    InstanceRunID           SMALLINT       NOT NULL,
    GameID                  MEDIUMINT      NOT NULL, 
    PRIMARY KEY (VideoID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Venue (
    VenueID                 SMALLINT       AUTO_INCREMENT,
    VenueName               VARCHAR(50)    NOT NULL, 
    VenueDescription        TEXT           DEFAULT NULL,
    PowerOutlets            SMALLINT       DEFAULT NULL,
    LightingNotes           TEXT           DEFAULT NULL,
    SupervisorID            SMALLINT       NOT NULL,
    PRIMARY KEY (VenueID),
    FOREIGN KEY (SupervisorID) REFERENCES Player(PlayerID)
	    ON DELETE RESTRICT
	    ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Equipment (
    EquipmentID             SMALLINT       AUTO_INCREMENT,
    ModelAndMake            VARCHAR(45)    DEFAULT NULL,
    EquipmentReview         TEXT           DEFAULT NULL,
    ProcessorSpeed          VARCHAR(45)    DEFAULT NULL,
    PRIMARY KEY (EquipmentID)
) ENGINE=InnoDB;


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


CREATE TABLE Viewer(
    ViewerID                INT UNSIGNED   AUTO_INCREMENT,
    ViewerType              CHAR(1)        DEFAULT "N" NOT NULL, 
    DateOfBirth             DATE           DEFAULT NULL,
    Email                   VARCHAR(50)    NOT NULL,
    UserName                VARCHAR(12)    NOT NULL,
    HashedPassword          CHAR(128)      NOT NULL,
    Salt                    CHAR(32)       NOT NULL,
    PRIMARY KEY (ViewerID)
) ENGINE=InnoDB;


CREATE TABLE CrowdFundingViewer(
    ViewerID                INT UNSIGNED   NOT NULL,
    FirstName               VARCHAR(45)    DEFAULT NULL,
    LastName                VARCHAR(45)    DEFAULT NULL,
    TotalAmountDonated      DECIMAL(9,2)   DEFAULT 0.00,
    PRIMARY KEY (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE PremiumViewer(
    ViewerID                INT UNSIGNED   NOT NULL,
    RenewalDate             DATE           NOT NULL,
    PRIMARY KEY (ViewerID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE ViewerOrder(
    ViewerOrderID           INT UNSIGNED   AUTO_INCREMENT,
    OrderDate               DATE           NOT NULL,
    ViewedStatus            CHAR(7)        NOT NULL,
    ViewerID                INT UNSIGNED   NOT NULL,
    PRIMARY KEY (ViewerOrderID),
    FOREIGN KEY (ViewerID) REFERENCES Viewer(ViewerID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE ViewerOrderLine(
    VideoID                 MEDIUMINT      NOT NULL, 
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
    PostalArea              VARCHAR(10)    NOT NULL,
    Country                 VARCHAR(50)    NOT NULL,
    PRIMARY KEY (AddressID)
) ENGINE=InnoDB;


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

CREATE TABLE InstanceEquipment(
    InstanceRunID          SMALLINT        NOT NULL,
    EquipmentID            SMALLINT        NOT NULL,
    PRIMARY KEY (InstanceRunID, EquipmentID),
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE InstancePlayer(
    PlayerID               SMALLINT        NOT NULL,
    InstanceRunID          SMALLINT        NOT NULL,
    PerformanceNotes       TEXT            DEFAULT NULL,
    PRIMARY KEY (InstanceRunID, PlayerID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (InstanceRunID) REFERENCES InstanceRun(InstanceRunID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE AccessCode(
    AccessCodeID          CHAR(32)        NOT NULL,
    Description           TEXT            DEFAULT NULL,
    PRIMARY KEY (AccessCodeID)
) ENGINE=InnoDB;


CREATE TABLE AccessCodeVideo(
    AccessCodeID         CHAR(32)         NOT NULL,
    VideoID              MEDIUMINT        NOT NULL,
    PRIMARY KEY (AccessCodeID, VideoID),
    FOREIGN KEY (AccessCodeID) REFERENCES AccessCode(AccessCodeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (VideoID) REFERENCES Video(VideoID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;
