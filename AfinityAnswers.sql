USE Rfam;
SELECT COUNT(*) FROM taxonomy WHERE species like '%Panthera tigris%';

SELECT ncbi_id FROM taxonomy WHERE species like '%Panthera tigris sumatrae%';

SELECT t.ncbi_id, t.species, rs.length
FROM taxonomy t
INNER JOIN rfamseq rs ON t.ncbi_id = rs.ncbi_id
WHERE species LIKE 'Oryza%'
ORDER BY length DESC
LIMIT 1;

SELECT f.description, fam.* FROM family f 
JOIN (SELECT rf.rfamseq_acc, MAX(rf.length) length, fr.rfam_acc 
	  FROM rfamseq rf JOIN full_region fr 
	  			ON rf.rfamseq_acc = fr.rfamseq_acc 
	  WHERE rf.length > 1000000
	  GROUP BY fr.rfam_acc) fam
ON fam.rfam_acc = f.rfam_acc
ORDER BY fam.length DESC
LIMIT 121, 15;