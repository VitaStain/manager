SELECT nb.title, COUNT(*) AS count FROM notebooks_notebook nn
LEFT JOIN notebooks_brand nb ON nb.id = nn.brand_id
GROUP BY nb.title 
ORDER BY count DESC;

