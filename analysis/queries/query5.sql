/*
Returns the percentage of restaurants that violate 04L, grouped by borough
(Evidence of mice or live mice present in facility's food and/or non-food areas.)
*/
SELECT inspections.borough, ( COUNT(DISTINCT(address)) / CAST(totals.count AS FLOAT) ) AS p
	FROM inspections,
		(
			SELECT COUNT(DISTINCT(address)) AS count, borough
				FROM inspections
			GROUP BY borough
		) AS totals 
		WHERE violation_code = '04L' 
			AND totals.borough = inspections.borough
	GROUP BY inspections.borough ORDER BY p DESC;


