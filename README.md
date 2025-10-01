# aiti_guru
# Пункт 1
  Выполнен. Таблицы бд находятся в src/models/models_for_tz.py в виде orm моделей
# Пункт 2
  Пункт 2.1
  
    SELECT
      c.id,
      c.name AS client_name,
      COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS total_amount
    FROM clients c
    LEFT JOIN orders o     ON o.client_id = c.id
    LEFT JOIN order_items oi ON oi.order_id = o.id
    GROUP BY c.id, c.name
    ORDER BY total_amount DESC;
  
  Пункт 2.2

    SELECT 
      parent.id,
      parent.name,
      COUNT(child.id) AS direct_children_count
    FROM categories parent
    LEFT JOIN categories child ON child.parent_id = parent.id
    GROUP BY parent.id, parent.name;

  Пункт 2.3.1

    CREATE OR REPLACE VIEW top_5_products_last_month AS
    WITH root_categories AS (
        WITH RECURSIVE category_path AS (
            SELECT id, parent_id, name, id as root_id, name as root_name
            FROM categories 
            WHERE parent_id IS NULL
        
        UNION ALL
        
        SELECT c.id, c.parent_id, c.name, cp.root_id, cp.root_name
        FROM categories c
        JOIN category_path cp ON c.parent_id = cp.id
    )
    SELECT id, root_name FROM category_path
    )
    SELECT 
        p.name AS product_name,
        rc.root_name AS top_level_category,
        SUM(oi.quantity) AS total_sold_units
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    JOIN products p ON oi.product_id = p.id
    LEFT JOIN root_categories rc ON p.category_id = rc.id
    WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
        AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY p.id, p.name, rc.root_name
    ORDER BY total_sold_units DESC
    LIMIT 5;
    
# Пункт 3
