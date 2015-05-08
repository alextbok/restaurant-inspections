/*
Returns the percentage of restaurants that violate 04L, grouped by zip code
(Evidence of mice or live mice present in facility's food and/or non-food areas.)
*/
SELECT inspections.zip, ( COUNT(DISTINCT(address)) / CAST(totals.count AS FLOAT) ) AS p, totals.count
	FROM inspections,
		(
			SELECT COUNT(DISTINCT(address)) AS count, zip
				FROM inspections
			GROUP BY zip
		) AS totals 
		WHERE violation_code = '04L' 
			AND totals.zip = inspections.zip
	GROUP BY inspections.zip ORDER BY p DESC;