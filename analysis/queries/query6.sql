/*
Returns the percentage of restaurants that violate 04L, grouped by cuisine type
(Evidence of mice or live mice present in facility's food and/or non-food areas.)
*/
SELECT inspections.cuisine_type, ( COUNT(DISTINCT(address)) / CAST(totals.count AS FLOAT) ) AS p
	FROM inspections,
		(
			SELECT COUNT(DISTINCT(address)) AS count, cuisine_type
				FROM inspections
			GROUP BY cuisine_type
			HAVING count > 5
		) AS totals 
		WHERE violation_code = '04L' 
			AND totals.cuisine_type = inspections.cuisine_type
	GROUP BY inspections.cuisine_type ORDER BY p DESC;