WITH notebooks(width, depth, height, count)
AS
(SELECT (5 * CEIL(width/5)) AS width,
        (5 * CEIL(depth/5)) AS depth,
        (5 * CEIL(height/5)) AS height,
        COUNT(title) AS count FROM notebooks_notebook
        GROUP BY width, depth, height)
SELECT width, depth, height, SUM(count) AS count FROM notebooks
GROUP BY width, depth, height
ORDER BY width, depth, height;
