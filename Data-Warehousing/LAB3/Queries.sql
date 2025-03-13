-- kpi 

-- FH, FC (30%)

SELECT TD.monthid, 									
       Sum(AU.flighthours)  AS FH, 
       Sum(AU.flightcycles) AS FC 
FROM   aircraftutilization AU, 
	   temporaldimension TD, 
       aircraftdimension AD
WHERE  AU.aircraftid = AD.id 
       AND AU.timeid = TD.id 
       AND AD.model = '777' 
GROUP  BY TD.monthid
ORDER  BY TD.monthid; 


-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------
-- ADOSS, ADOSU (30%)

SELECT M.Y,											
	   Sum(AU.scheduledoutofservice)   AS ADOSS, 
       Sum(AU.unscheduledoutofservice) AS ADOSU 
FROM   aircraftutilization AU, 
       months M, 
       temporaldimension TD 
WHERE  M.id = TD.monthid 
       AND AU.timeid = TD.id 
       AND AU.aircraftid = 'XY-WTR' 
GROUP  BY M.y; 


-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------
-- RRh, RRc, PRRh, PRRc, MRRh, MRRc (20%)

SELECT LR.monthid, 											
       1000 * ( marep + pirep ) / fh AS RRh, 
       100 * ( marep + pirep ) / fc  AS RRc, 
       1000 * pirep / fh             AS PRRh, 
       100 * pirep / fc              AS PRRc, 
       1000 * marep / fh             AS MRRh, 
       100 * marep / fc              AS MRRc 
FROM   (SELECT TD.monthid, 
               Sum(AU.flighthours)  AS FH, 
               Sum(AU.flightcycles) AS FC 
        FROM   temporaldimension TD, 
               aircraftdimension AD, 
               aircraftutilization AU 
        WHERE  AU.aircraftid = AD.id 
               AND AU.timeid = TD.id 
               AND AD.model = '777' 
        GROUP  BY TD.monthid) AU, 
       (SELECT L.monthid, 
               Sum(CASE 
                     WHEN PD.role = 'M' THEN L.counter 
                     ELSE 0 
                   END) AS MAREP, 
               Sum(CASE 
                     WHEN PD.role = 'P' THEN L.counter 
                     ELSE 0 
                   END) AS PIREP 
        FROM   logbookreporting L, 
               aircraftdimension AD, 
               peopledimension PD 
        WHERE  L.aircraftid = AD.id 
               AND PD.id = L.personid 
               AND AD.model = '777' 
        GROUP  BY L.monthid) LR
WHERE  AU.monthid = LR.monthid;

-----------------------------------------------------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------
-- MRRh, MRRc (20%)

SELECT LR.model, 					
       1000 * marep / fh AS MRRh, 
       100 * marep / fc  AS MRRc 
FROM   (SELECT AD.model, 
               Sum(AU.flighthours)  AS FH, 
               Sum(AU.flightcycles) AS FC 
        FROM   aircraftdimension AD, 
               aircraftutilization AU 
        WHERE  AU.aircraftid = AD.id 
        GROUP  BY AD.model) AU, 
        
       (SELECT AD.model, 
               Sum(CASE WHEN PD.role = 'M' THEN L.counter ELSE 0 END) AS MAREP
        FROM   logbookreporting L, 
               aircraftdimension AD, 
               peopledimension PD 
        WHERE  L.aircraftid = AD.id 
               AND PD.airport = 'KRS' 
               AND PD.id = L.personid 
        GROUP  BY AD.model) LR 
WHERE  AU.model = LR.model; 


