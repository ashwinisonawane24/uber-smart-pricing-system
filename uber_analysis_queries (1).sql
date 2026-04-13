

--UBER SMART PRICING SYSTEM -----> SQL Analysis Queries
---Author: Ashwini Sonawane
---Dataset: 200,000 Uber Rides (2009-2015)


-----------------------
--Q1: Peak Demand Hours
--Business Question: Which hours have highest demand?

SELECT 
    hour,
    COUNT(*) as total_rides,
    ROUND(COUNT(*) * 100.0 / 
    (SELECT COUNT(*) FROM uber), 2) as demand_percentage
FROM uber
GROUP BY hour
ORDER BY total_rides DESC
LIMIT 10;

-------------------------

--Q2: Average Fare Per Hour
--Business Question: When do riders pay most?


SELECT 
    hour,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(MIN(fare_amount), 2) as min_fare,
    ROUND(MAX(fare_amount), 2) as max_fare
FROM uber
WHERE fare_amount > 0
GROUP BY hour
ORDER BY avg_fare DESC;

---------------------------

--Q3: Peak vs Non Peak Comparison
--Business Question: How much revenue do peak hours generate?
--KEY FINDING: Non peak fare > Peak fare!


SELECT
    CASE 
        WHEN hour BETWEEN 7 AND 10 THEN 'Morning Peak'
        WHEN hour BETWEEN 16 AND 20 THEN 'Evening Peak'
        ELSE 'Non Peak'
    END as time_category,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue
FROM uber
WHERE fare_amount > 0
GROUP BY time_category
ORDER BY total_revenue DESC;

------------------------------


--Q4: Rides by Day of Week
--Business Question: Which days perform best?


SELECT
    day_of_week,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue
FROM uber
WHERE fare_amount > 0
GROUP BY day_of_week
ORDER BY total_rides DESC;

-------------------------

--Q5: Top 5 Revenue Generating Hours
--Business Question: Which hours drive most revenue?


SELECT
    hour,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue,
    ROUND(SUM(fare_amount) * 100.0 /
         (SELECT SUM(fare_amount) FROM uber
          WHERE fare_amount > 0), 2) as revenue_percentage
FROM uber
WHERE fare_amount > 0
GROUP BY hour
ORDER BY total_revenue DESC
LIMIT 5;

------------------------------------

--Q6: Passenger Count Analysis
--Business Question: Who rides Uber most?
--KEY FINDING: Solo riders = 69% of business

SELECT
    passenger_count,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue,
    ROUND(COUNT(*) * 100.0 /
         (SELECT COUNT(*) FROM uber), 2) as ride_percentage
FROM uber
WHERE fare_amount > 0
AND passenger_count > 0
GROUP BY passenger_count
ORDER BY total_rides DESC;

----------------------------------------------

--Q7: Solo Rider Peak Hours
--Business Question: When do solo riders travel most?

SELECT
    hour,
    COUNT(*) as solo_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as revenue
FROM uber
WHERE passenger_count = 1
AND fare_amount > 0
GROUP BY hour
ORDER BY solo_rides DESC;

-------------------------------------

--Q8: Yearly Revenue Trend
--Business Question: How has business grown over years?
--KEY FINDING: Competition impact visible from 2013

SELECT
    year,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue
FROM uber
WHERE fare_amount > 0
GROUP BY year
ORDER BY year ASC;

---------------------------------------------------

--Q9: Monthly Demand Patterns
--Business Question: Which months are busiest?
--NOTE: Excluded 2015 (incomplete year - Jan to Jun only)


SELECT
    month,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue
FROM uber
WHERE fare_amount > 0
AND year != 2015
GROUP BY month
ORDER BY month ASC;

-----------------------------------------------------

--Q10: Trip Category Analysis
--Business Question: What type of trips dominate?
--KEY FINDING: Premium trips earn 9x more per ride


SELECT
    CASE
        WHEN fare_amount BETWEEN 0 AND 10
            THEN 'Short Trip (0-$10)'
        WHEN fare_amount BETWEEN 10 AND 20
            THEN 'Medium Trip ($10-$20)'
        WHEN fare_amount BETWEEN 20 AND 50
            THEN 'Long Trip ($20-$50)'
        WHEN fare_amount > 50
            THEN 'Premium Trip ($50+)'
    END as trip_category,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare,
    ROUND(SUM(fare_amount), 2) as total_revenue,
    ROUND(COUNT(*) * 100.0 /
         (SELECT COUNT(*) FROM uber
          WHERE fare_amount > 0), 2) as percentage
FROM uber
WHERE fare_amount > 0
GROUP BY trip_category
ORDER BY total_rides DESC;

-----------------------------------------------

--Q11: Time Slot vs Trip Type
--Business Question: What rides happen when?
--KEY FINDING: 3 customer personas identified

SELECT
    CASE
        WHEN hour BETWEEN 4 AND 6
            THEN 'Early Morning'
        WHEN hour BETWEEN 7 AND 10
            THEN 'Morning Peak'
        WHEN hour BETWEEN 11 AND 15
            THEN 'Afternoon'
        WHEN hour BETWEEN 16 AND 20
            THEN 'Evening Peak'
        WHEN hour BETWEEN 21 AND 23
            THEN 'Late Night'
        ELSE 'Midnight'
    END as time_slot,
    CASE
        WHEN fare_amount BETWEEN 0 AND 10
            THEN 'Short'
        WHEN fare_amount BETWEEN 10 AND 20
            THEN 'Medium'
        ELSE 'Long/Premium'
    END as trip_type,
    COUNT(*) as total_rides,
    ROUND(AVG(fare_amount), 2) as avg_fare
FROM uber
WHERE fare_amount > 0
GROUP BY time_slot, trip_type
ORDER BY total_rides DESC
LIMIT 10;

