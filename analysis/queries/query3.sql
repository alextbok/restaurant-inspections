/*
Returns the most common violations for each borough
*/
SELECT inspections.borough, violation_code, description, ( COUNT(violation_code) / CAST(counts.c AS FLOAT) ), COUNT(violation_code) as p 
	FROM inspections, violations,
		(
			SELECT borough, COUNT(*) AS c
				FROM inspections
			GROUP BY borough
		) AS counts
		WHERE violation_code != '' 
			AND violation_code = code
			AND counts.borough = inspections.borough
	GROUP BY inspections.borough, violation_code ORDER BY inspections.borough, p DESC;