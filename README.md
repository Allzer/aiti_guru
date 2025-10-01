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
    
# Пункт 3
