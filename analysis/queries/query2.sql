/*
Returns the most common violations for each cuisine type
*/
SELECT inspections.cuisine_type, violation_code, description, ( COUNT(violation_code) / CAST(counts.c AS FLOAT) ) as p 
	FROM inspections, violations,
		(
			SELECT cuisine_type, COUNT(*) AS c
				FROM inspections
					WHERE cuisine_type != '' 
			GROUP BY cuisine_type
		) AS counts
		WHERE inspections.cuisine_type != '' 
			AND violation_code != '' 
			AND violation_code != '10F' 
			AND violation_code = code
			AND counts.cuisine_type = inspections.cuisine_type
	GROUP BY inspections.cuisine_type, violation_code ORDER BY p DESC;