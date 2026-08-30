-- Module 1: Data Exploration & Profiling

-- Q1 
    -- Total Transactions 

SELECT COUNT(transaction_id) AS total_transactions
FROM bank_fraud;

    -- Total Customers

SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM BANK_FRAUD;

    -- Total Fraud Transactions 
SELECT COUNT(*) AS total_fraud_transactions
FROM BANK_FRAUD
WHERE is_fraud = TRUE;

    -- Fraud Percentage 

SELECT 
    ROUND(
        COUNT_IF(is_fraud = TRUE) * 100.0 / COUNT(*),2
    ) AS fraud_percentage
FROM bank_fraud;

SELECT COUNT(
    CASE 
        WHEN is_fraud = TRUE 
        THEN 1
    END
) * 100 / COUNT(*) AS fraud_percentage
FROM bank_fraud;


-- Q2 . Find the top 10 countries by transaction volume.

SELECT
    country,
    COUNT(transaction_id) AS transaction_volume
FROM BANK_FRAUD
GROUP BY country
ORDER BY transaction_volume DESC
LIMIT 10;

-- Q3. Find the top 10 cities generating the highest transaction value.

SELECT 
    city,
    SUM(transaction_amount) AS transaction_value
FROM bank_fraud
GROUP BY city
ORDER BY transaction_value DESC
LIMIT 10;


-- Q4. Generate a complete data profiling report showing:
     -- Column Name
    -- Distinct Values
    -- Null Count


SELECT
    LISTAGG(
        'SELECT ''' || column_name || ''' AS column_name, ' ||
        'COUNT(DISTINCT "' || column_name || '") AS distinct_values, ' ||
        'COUNT(*) - COUNT("' || column_name || '") AS null_count ' ||
        'FROM BANK_FRAUD',
        ' UNION ALL '
    ) WITHIN GROUP (ORDER BY ordinal_position) AS profiling_query
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'BANK_FRAUD';


-- Q5. Determine the percentage distribution of transactions by:
    -- Payment Method 
SELECT 
    payment_method,
    ROUND(
        COUNT(transaction_id)
        / SUM(COUNT(transaction_id)) OVER () * 100.0,
        2
    ) AS percentage_distribution
FROM BANK_FRAUD
GROUP BY payment_method
ORDER BY percentage_distribution DESC;

    -- Device Type 
SELECT 
    device_type,
    ROUND(
        COUNT(transaction_id)
        / SUM(COUNT(transaction_id)) OVER() * 100.0,
    2
    ) AS percentage_distribution
FROM bank_fraud
GROUP BY device_type
ORDER BY percentage_distribution DESC;

    -- Merchant Category 

SELECT 
    merchant_category,
    ROUND(
        COUNT(transaction_id)
        / SUM(COUNT(transaction_id)) OVER() * 100.0,
        2
    ) AS percentage_distribution
FROM bank_fraud,
GROUP BY merchant_category
ORDER BY percentage_distribution DESC;


-- Module 2: Customer Behavior Analytics
-- Q6. Identify the top 20 customers by:
-- SUM(transaction_amount)

SELECT 
    customer_id AS top_customers,
    ROUND(SUM(transaction_amount), 2) AS total_transaction_amount
FROM bank_fraud
GROUP BY customer_id
ORDER BY total_transaction_amount DESC
LIMIT 20;

---- Q7. Calculate average transaction amount by age group:
-- 18-25
-- 26-35
-- 36-50
-- 51-65
-- 65+

SELECT 
    CASE
        WHEN customer_age < 25 THEN 'Young'
        WHEN customer_age < 35 THEN 'Not that young anymore'
        WHEN customer_age < 50 THEN 'Unfortunately old'
        WHEN customer_age < 65 THEN 'Poor you'
        ELSE 'Very old'
    END AS age_group,
    ROUND(avg(transaction_amount),2) AS avg_transaction_amount
FROM bank_fraud
GROUP BY age_group
ORDER BY avg_transaction_amount DESC;

    
-- Q8. Determine which age group has the highest fraud rate.

SELECT 
    CASE
        WHEN customer_age < 25 THEN 'Young'
        WHEN customer_age < 35 THEN 'Not that young anymore'
        WHEN customer_age < 50 THEN 'Unfortunately old'
        WHEN customer_age < 65 THEN 'Poor you'
        ELSE 'Very old'
    END AS age_group,
    ROUND(
        COUNT_IF(is_fraud = TRUE) 
        / COUNT(transaction_id) * 100.0,
        2
    ) AS fraud_rate
FROM bank_fraud
GROUP BY age_group
ORDER BY fraud_rate DESC;

-- Q9. Find customers with:
-- High Balance

SELECT 
    customer_id,
    MAX(account_balance) AS account_balance
FROM bank_fraud
GROUP BY customer_id
ORDER BY account_balance DESC;



-- Low Transaction Frequency

SELECT
    customer_id,
    COUNT(transaction_id) AS total_transactions
FROM bank_fraud
GROUP BY customer_id
ORDER BY total_transactions ASC;


-- Potential dormant accounts
----- For example: no transaction in the last 90 days

-- dataset is up to date
SELECT
    customer_id,
    MAX(transaction_date) AS last_transaction_date
FROM bank_fraud
GROUP BY customer_id
HAVING MAX(transaction_date) < dateadd(DAY,-90,CURRENT_DATE())
ORDER BY last_transaction_date ASC;

-- if dataset is not up to date 

SELECT
    customer_id,
    MAX(TRANSACTION_DATE) AS last_transaction_date
FROM bank_fraud
GROUP BY customer_id
HAVING MAX(TRANSACTION_DATE) < 
        dateadd
            (DAY, 
            -90,
            (SELECT MAX(TRANSACTION_DATE)
            FROM bank_fraud)
        )
ORDER BY last_transaction_date ASC;

-- Q10. Calculate average account balance and credit score by country.

SELECT
    country,
    ROUND(avg(account_balance),2) AS avg_account_balance,
    ROUND(avg(credit_score), 2) AS avg_credit_score   
FROM bank_fraud
GROUP BY country
ORDER BY avg_credit_score DESC;

-- Module 3: Fraud Pattern Analysis
-- Q11. Calculate fraud rate by:
        --          Merchant Category 

SELECT
    merchant_category,
    ROUND(COUNT_IF(is_fraud = TRUE)
    / COUNT(transaction_id) * 100.0, 2) AS fraud_rate
FROM bank_fraud
GROUP BY merchant_category
ORDER BY fraud_rate DESC;


--- Q12. Determine fraud rate by:
-- Payment Method 

SELECT
    payment_method,
    ROUND(COUNT_IF(is_fraud = TRUE)
    / COUNT(transaction_id) * 100.0, 2) AS fraud_rate
FROM bank_fraud
GROUP BY payment_method
ORDER BY fraud_rate DESC;

-- Q13. Determine fraud rate by:
-- Device Type 

SELECT
    device_type,
    ROUND(COUNT_IF(is_fraud = TRUE)
    / COUNT(transaction_id) * 100.0, 2) AS fraud_rate
FROM bank_fraud
GROUP BY device_type
ORDER BY fraud_rate DESC;

-- Q14. Find the most common fraud type.
-- Output:
-- fraud_type
-- count
-- percentage

SELECT
    fraud_type,
    COUNT(*) AS count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(),
        2
    ) AS percentage
FROM bank_fraud
WHERE is_fraud = TRUE
group by fraud_type
ORDER BY count DESC;

-- Q15. Analyze fraud transactions occurring during:
-- Night vs Day

SELECT
    COUNT_IF(is_night_transaction = TRUE) AS night_transaction,
    COUNT_IF(is_night_transaction = FALSE) AS day_transaction 
FROM bank_fraud
WHERE is_fraud = TRUE;

-- 2. Weekend vs Weekday

SELECT
    COUNT_IF(is_weekend = TRUE) AS weekend_transaction,
    COUNT_IF(is_weekend = FALSE) AS weekday_transaction 
FROM bank_fraud
WHERE is_fraud = TRUE;

SELECT 
    is_weekend,
    COUNT(*) AS transaction_count
FROM bank_fraud
WHERE is_fraud = TRUE
GROUP BY is_weekend
ORDER BY is_weekend desc;


