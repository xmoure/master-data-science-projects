Begin
for t in (select table_name from user_tables) loop
execute immediate ('drop table '||t.table_name||' cascade constraints');
end loop;
for c in (select cluster_name from user_clusters) loop
execute immediate ('drop cluster '||c.cluster_name);
end loop;
for i in (select index_name from user_indexes) loop
execute immediate ('drop index '||i.index_name);
end loop;
execute immediate ('purge recyclebin');
End;

ALTER SESSION SET star_transformation_enabled = TRUE;
-- create tables 

CREATE TABLE Months (
ID CHAR(7),
y NUMBER(4) NOT NULL
) PCTFREE 0 ENABLE ROW MOVEMENT;

CREATE TABLE TemporalDimension (
ID DATE,
monthID CHAR(7) NOT NULL
) PCTFREE 0 ENABLE ROW MOVEMENT;;


CREATE TABLE AircraftDimension (
ID CHAR(6),                            
model VARCHAR2(100) NOT NULL,          
manufacturer VARCHAR2(100) NOT NULL   
)PCTFREE 0 ENABLE ROW MOVEMENT;

CREATE TABLE AircraftUtilization (
aircraftID CHAR(6),
timeID DATE,
scheduledOutOfService NUMBER(2),
unScheduledOutOfService NUMBER(2),
flightHours NUMBER(2),
flightCycles NUMBER(2),
delays NUMBER(2),
delayedMinutes NUMBER(3),
cancellations NUMBER(2)
) PCTFREE 0 ENABLE ROW MOVEMENT;

CREATE TABLE PeopleDimension (
ID CHAR(6),                                       
airport CHAR(3),
role CHAR(1) CHECK (role IN ('P','M')) NOT NULL
)PCTFREE 0 ENABLE ROW MOVEMENT;

CREATE TABLE LogBookReporting (
aircraftID CHAR(6),
monthID CHAR(7),
personID CHAR(6),
counter NUMBER(2) NOT NULL
) PCTFREE 0 ENABLE ROW MOVEMENT;


-- generate data 

DECLARE
  i INTEGER;
  j INTEGER;
  k INTEGER;
  nextDate DATE;
  nextMonth varchar2(6);
  manufacturer varchar2(6);
  model varchar2(25);
  maxPeople CONSTANT INTEGER := 100;  
  maxTemporal CONSTANT INTEGER := 5000;   
  l_start_date DATE := DATE'2004-01-01';
 
  type aircraftarray is varray(20) of varchar2(6);
  aircrafts CONSTANT aircraftarray := aircraftarray('XY-WTR', 'XY-VWK', 'XY-OKG','XY-HNS','XY-QLY','XY-XTT','XY-QXN','XY-JJQ','XY-ZSE','XY-XVI','XY-HXO','XY-IOL','XY-WBH','XY-EYQ','XY-OSF','XY-KKF','XY-ZHR','XY-HCI','XY-XPV','XY-VYU'); 
   
  type modelBoeingarray is varray(4) of varchar2(25);
  modelsBoeing CONSTANT modelBoeingarray := modelBoeingarray('767','777','747','737');
 
  type modelAirbusarray is varray(6) of varchar2(25);
  modelsAirbus CONSTANT modelAirbusarray := modelAirbusarray('A340','A330','A321','A330neo','A320neo family','A350 XWB');
 
  type manufacturerarray is varray(2) of varchar2(6);
  manufacturers CONSTANT manufacturerarray := manufacturerarray('Boeing','Airbus');
 
  type airportarray is varray(100) of varchar2(3);
  airports CONSTANT airportarray := airportarray('AGP','SKP','TSE','ESB','VKO','IEV','TIV','FRA','DUB','PDL','GYD','KIV','TRD','CLJ','TLL','OLB','BHX','KRS','DME','DRS','VNO','TFS','NUE','GDN','OVD','BGY','ORY','FNC','MSQ','LPL','TLS','TPS','RVN','PUY','AJA','LWO','CIA','GVA','LTN','HUY','BIQ','DBV','REU','BOO','ODS','RHO','CIY','BJV','BSL','GLA','EIN','LUG','BRQ','BRN','CTA','AAR','TSF','KUN','ZTH','WAW','BIO','LYS','PMO','CFU','OSL','BES','AER','ZAZ','FUE','LNZ','FMO','LIL','SVG','PMI','GOA','INI','LJU','IST','SVX','KBP','XRY','TZX','SEN','OVB','FCO','OST','VLC','SCQ','PFO','HAJ','ALC','PSR','ORK','AAL','EXT','BIA','MAN','BRS','SXF','FAO');
 
  type rolearray is varray(2) of varchar2(1);
  roles CONSTANT rolearray := rolearray('P','M');
  
BEGIN
DBMS_RANDOM.seed(0);

-- Insertions in AircraftDimentsion
FOR i IN 1..(aircrafts.count) LOOP
  manufacturer := manufacturers(dbms_random.value(1,2));
  IF (manufacturer = 'Airbus') THEN
  INSERT INTO AIRCRAFTDIMENSION(ID, MODEL, MANUFACTURER) VALUES (aircrafts(i), modelsAirbus(dbms_random.value(1,6)), manufacturer);
  ELSIF (manufacturer = 'Boeing') THEN 
  INSERT INTO AIRCRAFTDIMENSION(ID, MODEL, MANUFACTURER) VALUES (aircrafts(i), modelsBoeing(dbms_random.value(1,4)), manufacturer);
  END IF;
 END LOOP;
 
 -- Insertions in PeopleDimension
FOR i IN 1..(maxPeople) LOOP
  INSERT INTO PEOPLEDIMENSION(ID, AIRPORT, "ROLE") VALUES (i, airports(dbms_random.value(1,100)), roles(dbms_random.value(1,2)));
  END LOOP;   
 

 -- Insertions in TemporalDimensions and Months
 nextMonth :=  CONCAT(LPAD(EXTRACT(MONTH FROM l_start_date),2,'0'), LPAD(EXTRACT(YEAR FROM l_start_date),4,'0'));
 INSERT INTO MONTHS(ID,Y) VALUES (nextMonth, SUBSTR(nextMonth,LENGTH(nextMonth)-3,4));
 FOR i IN 1..maxTemporal LOOP  
  nextDate := l_start_date + i;    
  IF CONCAT(LPAD(EXTRACT(MONTH FROM nextDate),2,'0'), LPAD(EXTRACT(YEAR FROM nextDate),4,'0')) <> nextMonth THEN 
      nextMonth :=  CONCAT(LPAD(EXTRACT(MONTH FROM nextDate),2,'0'), LPAD(EXTRACT(YEAR FROM nextDate),4,'0'));
	  INSERT INTO MONTHS(ID,Y) VALUES (nextMonth, SUBSTR(nextMonth,LENGTH(nextMonth)-3,4));
  END IF; 
  INSERT INTO TEMPORALDIMENSION(ID, MONTHID) VALUES (nextDate, nextMonth); 
 END LOOP;
  
-- Insertions in LogBookReporting
 nextMonth :=  CONCAT(LPAD(EXTRACT(MONTH FROM l_start_date),2,'0'), LPAD(EXTRACT(YEAR FROM l_start_date),4,'0'));
 FOR i IN 1..aircrafts.count LOOP
   FOR k IN 1..maxPeople LOOP
	 FOR j IN 1..maxTemporal LOOP
	     nextDate := l_start_date + j;
	     IF CONCAT(LPAD(EXTRACT(MONTH FROM nextDate),2,'0'), LPAD(EXTRACT(YEAR FROM nextDate),4,'0')) <> nextMonth THEN 
		    nextMonth :=  CONCAT(LPAD(EXTRACT(MONTH FROM nextDate),2,'0'), LPAD(EXTRACT(YEAR FROM nextDate),4,'0'));	
		 ELSE CONTINUE;
		 END IF;		 
		  INSERT INTO LOGBOOKREPORTING(AIRCRAFTID, MONTHID, PERSONID, COUNTER) VALUES (
		    aircrafts(i),
		    nextMonth,
		    k,
		    CAST(dbms_random.value(1,50) AS INT) );
		 END LOOP;
	 END LOOP;
 END LOOP;

-- Insertions in AircraftUtilization
FOR i IN 1..aircrafts.count LOOP
	 FOR j IN 1..maxTemporal LOOP		
	 nextDate := l_start_date + j;
	  INSERT INTO AIRCRAFTUTILIZATION(AIRCRAFTID, TIMEID, FLIGHTHOURS, FLIGHTCYCLES, DELAYS, DELAYEDMINUTES, CANCELLATIONS, SCHEDULEDOUTOFSERVICE, UNSCHEDULEDOUTOFSERVICE) VALUES (
	    aircrafts(i),
	    nextDate,	    
	  	CAST(dbms_random.value(1,24) AS INT),
	    CAST(dbms_random.value(1,5) AS INT),
	    CAST(dbms_random.value(1,5) AS INT),
	    CAST(dbms_random.value(1,3) AS INT),
	    CAST(dbms_random.value(0,2) AS INT),
	    CAST(dbms_random.value(1,5) AS INT),
	    CAST(dbms_random.value(1,5) AS INT));		 
	 END LOOP;
END LOOP;

UPDATE PEOPLEDIMENSION SET airport=null WHERE ROLE='P';

END;

COMMIT;


ALTER TABLE AIRCRAFTDIMENSION SHRINK SPACE;
ALTER TABLE PEOPLEDIMENSION SHRINK SPACE;
ALTER TABLE TEMPORALDIMENSION SHRINK SPACE;
ALTER TABLE MONTHS SHRINK SPACE;
ALTER TABLE AIRCRAFTUTILIZATION SHRINK SPACE;
ALTER TABLE LOGBOOKREPORTING SHRINK SPACE;

-- adding indexes
--ALTER TABLE AIRCRAFTUTILIZATION minimize RECORDS_PER_BLOCK;
--ALTER TABLE LOGBOOKREPORTING minimize RECORDS_PER_BLOCK;
--ALTER TABLE TEMPORALDIMENSION MOVE;
--ALTER TABLE MONTHS MOVE;
--ALTER TABLE AircraftDimension MOVE;
--ALTER TABLE PEOPLEDIMENSION MOVE;

--CREATE INDEX monthid ON TEMPORALDIMENSION (monthid) PCTFREE 33; 
--CREATE BITMAP INDEX flighhours ON AIRCRAFTUTILIZATION(flighthours) PCTFREE 0; 
--CREATE BITMAP INDEX flightcycles ON AIRCRAFTUTILIZATION(flightcycles) PCTFREE 0; 
CREATE BITMAP INDEX aircraftid ON AIRCRAFTUTILIZATION(aircraftid) PCTFREE 0;
ALTER TABLE AIRCRAFTDIMENSION ADD PRIMARY KEY (id) USING
INDEX PCTFREE 33;
CREATE BITMAP INDEX aircraftiModel ON AIRCRAFTUTILIZATION(a2.MODEL)
FROM AIRCRAFTUTILIZATION a, AIRCRAFTDIMENSION a2
WHERE a.AIRCRAFTID =a2.ID PCTFREE 0;


--ALTER TABLE PEOPLEDIMENSION ADD PRIMARY KEY (ID) USING
--INDEX PCTFREE 33;
--CREATE BITMAP INDEX AIRCRAFTIDLOGROLE ON LOGBOOKREPORTING (PD.AIRPORT)
--FROM LOGBOOKREPORTING L, PEOPLEDIMENSION PD
--WHERE PD.id = L.personid  PCTFREE 0;
--DROP INDEX AIRCRAFTIDLOGROLE;

CREATE BITMAP INDEX AIRCRAFTIDLOG ON LOGBOOKREPORTING(AIRCRAFTID) PCTFREE 0; 
CREATE BITMAP INDEX PERSONID ON LOGBOOKREPORTING(PERSONID) PCTFREE 0;

--CREATE BITMAP INDEX counter ON LOGBOOKREPORTING(counter) PCTFREE 0;
--CREATE BITMAP INDEX monthid ON LOGBOOKREPORTING(monthid) PCTFREE 0;
--DROP INDEX monthid;
--DROP INDEX counter;

-- update statistics

DECLARE
esquema VARCHAR2(100);
CURSOR c IS SELECT TABLE_NAME FROM USER_TABLES WHERE TABLE_NAME NOT LIKE 'SHADOW_%';
BEGIN
SELECT '"'||sys_context('USERENV', 'CURRENT_SCHEMA')||'"' INTO esquema FROM dual;
FOR taula IN c LOOP
  DBMS_STATS.GATHER_TABLE_STATS( 
    ownname => esquema, 
    tabname => taula.table_name, 
    estimate_percent => NULL,
    method_opt =>'FOR ALL COLUMNS SIZE REPEAT',
    granularity => 'GLOBAL',
    cascade => TRUE
    );
  END LOOP;
END;


-- check occupied space
SELECT SUM(blocks) FROM USER_TS_QUOTAS;

