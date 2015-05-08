/*
Returns the most commonly co-occurring violations (two violations "co-occur" 
if a single restaurant has violated both)
*/
SELECT DISTINCT COUNT(*) as cnt, (CASE WHEN i1.violation_code < i2.violation_code THEN i1.violation_code ELSE i2.violation_code END),
								(CASE WHEN i1.violation_code < i2.violation_code THEN i2.violation_code ELSE i1.violation_code END),
								(CASE WHEN i1.violation_code < i2.violation_code THEN v1.description ELSE v2.description END),
								(CASE WHEN i1.violation_code < i2.violation_code THEN v2.description ELSE v1.description END)
	FROM inspections AS i1, inspections AS i2, violations AS v1, violations AS v2 
		WHERE i1.name = i2.name 
			AND i1.address = i2.address
			AND i1.violation_code = v1.code 
			AND i2.violation_code = v2.code
			AND i1.violation_code != i2.violation_code 
			AND i1.violation_code != '99B'
			AND i2.violation_code != '99B'
GROUP BY i1.violation_code, i2.violation_code ORDER BY cnt DESC;