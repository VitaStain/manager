SELECT nb.title, COUNT(nn.title) AS count FROM notebooks_notebook nn
INNER JOIN notebooks_brand nb ON nb.id = nn.brand_id
GROUP BY nb.title 
ORDER BY count DESC;
