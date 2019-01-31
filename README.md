# ATLAS_API

This an an API that accepts as an input user application data for customers looking to obtain a loan and returns their suitability for the loan with a 1 or 0. 1 represents being suitable for the loan while 0 represent not being suitable for the loan.
 
 
 ### Data Dictionary
```text
Age (numeric)
Sex (text: male, female)
Job (numeric: 0 - unskilled and non-resident, 1 - unskilled and resident, 2 - skilled, 3 - highly skilled)
Housing (text: own, rent, or free)
Saving accounts (text - little, moderate, quite rich, rich)
Checking account (numeric, in DM - Deutsch Mark)
Credit amount (numeric, in DM)
Duration (numeric, in month)
Purpose (text: car, furniture/equipment, radio/TV, domestic appliances, repairs, education, business, vacation/others)
```
 
 
 #### *Sample input for the API*
 

```python
{
	"Saving accounts":"little", 
	 "Checking account":"little",
	 "Age":67,
	 "Job": 3,
	 "Housing":"rent",
	 "Duration": 12,
	 "Purpose": "furniture/equipment",
	 "Sex": "female",
	 "Credit amount":1200
}
```


#### *Sample Output*
```python
{
    "status": "success",
    "code": 200,
    "result": {
        "prediction": "1"
    }
 ```
 
 
 #### *API URL*
 
The api endpoint is _https://atlas-api-loan.herokuapp.com/model_ and a post request should be made.
    
  
  
    
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
