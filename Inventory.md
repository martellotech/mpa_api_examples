# Automating the flow of Reports.
Martello has the ability to schedule the distribution of reports via email, but this can be tricky when the data from the report is required by an external system.   In order to send the data from a Martello inventory report into an external inventory system many customers would prefer using scripts to get the Martello data and load it into the target system.

This example shows a simple technique for this.

## Configure the report that you wish to load.
Navigate to the report you wish to automate.  Set all columns and save the view you wish to export.

## Press the Export Button
Press the <img src="./docs/SNOW REST/Export Button.PNG" width=60> button.

## Confirm that the CSV file matches your requirements
## Capture the export URL
* Right click in the browser window and pick "Inspect".  This example is done with a Chrome browser, but very similar capabilities are available in other browsers.
* With "Inspect" open, choose the network tab.   Clear the list of requests.
* Click on the "Cownload CSV" button on the report.
* Right click on the URL "fetch". 
<img src="./docs/SNOW REST/Capture the URL.PNG" width=900>

* Select "Copy->URL"
* Save this URL in a text file.
* It should look like this:
<style>
  code {
    white-space : pre-wrap !important;
    word-break: break-all;
  }
</style>
```
https://mw5-init.marwatch.net/central/rest/containers/349907fc-8d31-4497-9104-79d34436c41d/queries/container_inventory_mivb_inventory?current_user_guid=e7ed5481-6373-4e5d-9027-32b3534fdd0c&format=csv&graphType=table&params=%7B%22take%22%3A50%2C%22skip%22%3A0%2C%22page%22%3A1%2C%22pageSize%22%3A50%2C%22sort%22%3A%5B%5D%2C%22group%22%3A%5B%5D%7D&selectedOption=IP+Sets&column%5B0%5D=ipbx_name&column%5B1%5D=number&column%5B2%5D=container_path&column%5B3%5D=name&column%5B4%5D=ipbx_type&column%5B5%5D=state&column%5B6%5D=ip_address&column%5B7%5D=mac_address&column%5B8%5D=subnet&column%5B9%5D=subnet_mask&column%5B10%5D=gateway&column%5B11%5D=vq_enabled&column%5B12%5D=primary&column%5B13%5D=secondary&column%5B14%5D=hw_version&column%5B15%5D=sw_version
```

## Use this URL in a script.
For example, this powershell script uses a report URL to fetch the CSV data

```
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Authorization", "(Basic Authorization Header for a valid user)")

$response = Invoke-RestMethod 'https://mw5-init.marwatch.net/central/rest/containers/72bbcf5b-f5d7-4435-9512-012eb39ee6a2/queries/container_inventory_mivb_inventory?current_user_guid=e7ed5481-6373-4e5d-9027-32b3534fdd0c&format=csv&graphType=table&params=%7B%22take%22%3A50%2C%22skip%22%3A0%2C%22page%22%3A1%2C%22pageSize%22%3A50%2C%22sort%22%3A%5B%5D%2C%22group%22%3A%5B%5D%7D&selectedOption=Users&column%5B0%5D=ipbx_name&column%5B1%5D=cluster_name&column%5B2%5D=container_path&column%5B3%5D=first_name&column%5B4%5D=last_name&column%5B5%5D=login&column%5B6%5D=department&column%5B7%5D=location&column%5B8%5D=user_comment' -Method 'GET' -Headers $headers
$response | ConvertTo-Json
# Do your own thing with the response
```

This is a curl example of the same script:
```
curl --location 'https://mw5-init.marwatch.net/central/rest/containers/72bbcf5b-f5d7-4435-9512-012eb39ee6a2/queries/container_inventory_mivb_inventory?current_user_guid=e7ed5481-6373-4e5d-9027-32b3534fdd0c&format=csv&graphType=table&params=%7B%22take%22%3A50%2C%22skip%22%3A0%2C%22page%22%3A1%2C%22pageSize%22%3A50%2C%22sort%22%3A%5B%5D%2C%22group%22%3A%5B%5D%7D&selectedOption=Users&column%5B0%5D=ipbx_name&column%5B1%5D=cluster_name&column%5B2%5D=container_path&column%5B3%5D=first_name&column%5B4%5D=last_name&column%5B5%5D=login&column%5B6%5D=department&column%5B7%5D=location&column%5B8%5D=user_comment' \
--header 'Authorization: ••••••'
```


## Generate a Basic Authorization Header.
This header is a string in the pattern 'Basic '+base64 encode of userid:password. You can generate this with a tool like postman (which can also generate scripts like the ones above), or by using an online tool like https://www.debugbear.com/basic-auth-header-generator

## Test the script, and do something with the output.
Replace the •••••• placeholders in the script(s) above and test them out.   
