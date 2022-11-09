/****** Script for SelectTopNRows command from SSMS  ******/

 --Create rent table.
CREATE TABLE Rents
       (Adress nvarchar(150) NOT NULL
      ,Rooms nvarchar(150) NOT NULL
      ,m2 nvarchar(150) NOT NULL
      ,Price nvarchar(150) NOT NULL
      ,Floor nvarchar(150) NOT NULL);
	  

  INSERT INTO Rents ([Adress]
      ,[Rooms]
      ,[m2]
      ,[Price]
      ,[Floor])
  SELECT * 
  FROM [PortfolioProject].[dbo].['Rigas centrs$']
  WHERE Price LIKE N'%€/mēn.'

  --clean rent price

  UPDATE [PortfolioProject].[dbo].[Rents]
  SET Price = REPLACE(Price, ',', '')
 
 UPDATE [PortfolioProject].[dbo].[Rents]
  SET Price = SUBSTRING(Price,1, CHARINDEX(' ', Price) -1)


UPDATE [PortfolioProject].[dbo].[Rents]
SET Price = CONCAT (Price, ' €')


  SELECT *, CONCAT ('  ', Floor )
  FROM [PortfolioProject].[dbo].[Rents]
 

  --check duplicates

-- WITH RowNumCTE AS (
-- SELECT *,
--	ROW_NUMBER() OVER ( PARTITION BY Adress,
--	Rooms, m2 , Price, Floor
--	ORDER BY Adress) row_num

--FROM [PortfolioProject].[dbo].[Rents]
-- )

--SELECT *
--FROM RowNumCTE
--WHERE row_num >1
--order by Adress

 --Seperate Sales
  CREATE TABLE Sales
       (Adress nvarchar(150) NOT NULL
      ,Rooms nvarchar(150) NOT NULL
      ,m2 nvarchar(150) NOT NULL
      ,Price nvarchar(150) NOT NULL
      ,Floor nvarchar(150) NOT NULL);

  INSERT INTO Sales
  SELECT * 
  FROM [PortfolioProject].[dbo].['Rigas centrs$']
  WHERE Price NOT LIKE N'%€/mēn.'

  --Clean price 


  UPDATE [PortfolioProject].[dbo].[Sales]
  SET Price = REPLACE(Price, ',', '.')
 

 --delete daily rentals and 2 more unused columns

 DELETE FROM [PortfolioProject].[dbo].[Sales]
 WHERE Price LIKE N'%€/%'

 DELETE FROM [PortfolioProject].[dbo].[Sales]
 WHERE Price LIKE N'%vēlos%'

 SELECT *, CONCAT ('  ', Floor )
 FROM [PortfolioProject].[dbo].[Sales]