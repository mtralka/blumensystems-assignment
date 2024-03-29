import enum

MANAGER_TYPE_COL_NAME = "mang_type"
DESIGNATION_TYPE_COL_NAME = "des_tp"
FEATURE_CLASS_COL_NAME = "featclass"


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return str(self.name)


class ManagerType(enum.Enum):
    STAT = "State Government"
    DIST = "District Government"
    LOC = "Local Government"
    NGO = "Non-Governmental Organization"
    FED = "Federal Government"
    PVT = "Private Entity"
    UNK = "Unknown"
    JNT = "Joint Management"
    TRIB = "Tribal Government"
    TERR = "Territorial Government"


class FeatureClass(enum.Enum):
    Designation = "Designation"
    Proclamation = "Proclamation"
    Marine = "Marine"
    Fee = "Fee"
    Easement = "Easement"


class DesignationType(enum.Enum):
    WSA = "Wilderness Study Area"
    WA = "Wilderness Area"
    WSR = "Wild and Scenic River"
    WPA = "Watershed Protection Area"
    UNKE = "Unknown Easement"
    UNK = "Unknown"
    SW = "State Wilderness"
    SRMA = "State Resource Management Area"
    SREC = "State Recreation Area"
    SP = "State Park"
    SOTH = "State Other or Unknown"
    SHCA = "State Historic or Cultural Area"
    SCA = "State Conservation Area"
    SDA = "Special Designation Area"
    RMA = "Resource Management Area"
    REA = "Research or Educational Area"
    RNA = "Research Natural Area"
    RECE = "Recreation or Education Easement"
    REC = "Recreation Management Area"
    RANE = "Ranch Easement"
    PREC = "Private Recreation or Education"
    PRAN = "Private Ranch"
    PPRK = "Private Park"
    POTH = "Private Other or Unknown"
    PHCA = "Private Historic or Cultural"
    PFOR = "Private Forest Stewardship"
    PCON = "Private Conservation"
    PAGR = "Private Agricultural"
    OCS = "Outer Continental Shelf Area"
    OTHE = "Other Easement"
    ND = "Not Designated"
    TRIBL = "Native American Land Area"
    NWR = "National Wildlife Refuge"
    NSBV = "National Scenic, Botanical or Volcanic Area"
    NT = "National Scenic or Historic Trail"
    NRA = "National Recreation Area"
    PUB = "National Public Lands"
    NP = "National Park"
    NM = "National Monument"
    NLS = "National Lakeshore or Seashore"
    NG = "National Grassland"
    NF = "National Forest"
    MIT = "Mitigation Land or Bank"
    MIL = "Military Land"
    MPA = "Marine Protected Area"
    LRMA = "Local Resource Management Area"
    LREC = "Local Recreation Area"
    LP = "Local Park"
    LOTH = "Local Other or Unknown"
    LHCA = "Local Historic or Cultural Area"
    LCA = "Local Conservation Area"
    IRA = "Inventoried Roadless Area"
    HCAE = "Historic or Cultural Easement"
    HCA = "Historic or Cultural Area"
    FORE = "Forest Stewardship Easement"
    FOTH = "Federal Other or Unknown"
    FACY = "Facility"
    CONE = "Conservation Easement"
    NCA = "Conservation Area"
    ACEC = "Area of Critical Environmental Concern"
    PROC = "Approved or Proclamation Boundary"
    AGRE = "Agricultural Easement"
    ACC = "Access Area"
