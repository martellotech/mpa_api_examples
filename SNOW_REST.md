# Process an MPA Alert as a SNOW Inbound email

There are 5 steps required on Service Now:

<img src="./docs/SNOW REST/SNOW Inbound Email Flow.PNG" width=500>

Step|Note
---|---
Inbound Email | Trigger on emails from MPA to SNOW
Extract MPA Parameters | The body of the email is parsable alarm data.
Create Inicdent Record | Create a SNOW incident for the alarm.
Update MPA | Send the Incident number and URL to MPA for "closed loop" linking.
Log | Create a log entry in Service Now.

# Create an Alert Profile on MPA
On a container whose alarms should be forwarded, create an Alert Profile with the filtering parameters you 
want to use. 

<img src="./docs/SNOW REST/MPA SNOW alert profile.PNG" width=800>

## Create a template that puts the parameters you want from MPA into a parsable format.
This example is kind of "minimal":
```JSON
{ "text": "${event.message}",
  "href": "${event.href}",
  "device":"${device.name}",
  "ticket":"$!{event.ticketNumber}"}
```


# Add the MPA email source as a SNOW user
Get the "From Email Address" value from  System->Configuration->SMTP Server.
Create a SNOW user like "MPA Alerts" with this email address.   There are probably other ways to 
make sure SNOW reads the emails, but this is effective and easy.

# Create a REST Message in SNOW
The REST message to update MPA uses basic authentication and the 'href' parameter of the alert to update
the ticket info fields in MPA.

## Create a Basic Auth Configuration in SNOW
```url
https://<your SNOW system>.service-now.com/sys_auth_profile_basic_list.do
```

## Create a REST Message to update Tickets
[Rest Messages page](https://ven04612.service-now.com/now/nav/ui/classic/params/target/sys_rest_message_list.do)
<img src="./docs/SNOW REST/REST.PNG">

## Use this REST Message in an Action
```javascript
(function execute(inputs, outputs) {
 try { 
 var r = new sn_ws.RESTMessageV2('MPA Update Ticket Information', 'Default PUT');
 r.setStringParameterNoEscape('href', inputs.href);
 body ={
    ticket: {
        status: "New",
        assignee: {
            name: "",
            GUID: ""
        },
        ticketinfo: {
            number: inputs.incident_number,
            URL:  "https://ven04612.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number="+inputs.incident_number
        }
    }
};
 r.setStringParameterNoEscape('content', JSON.stringify(body));
 r.setStringParameterNoEscape('user', 'e7ed5481-6373-4e5d-9027-32b3534fdd0c');
 gs.info("Updating MPA Ticket "+inputs.href)

 var response = r.execute();
 outputs.responsebody = response.getBody();
 outputs.httpstatus = response.getStatusCode();
 gs.info("Updating MPA Ticket "+inputs.href+" "+outputs.httpstatus)
}
catch(ex) {
 outputs.message = ex.message;
}
})(inputs, outputs);
```

# Invoke the action from a flow.
## Read Incomming Emails
Configure an incoming email trigger to read messages from the MPA source address.

## Extract MPA Parameters
Configure a flow to extract MPA parameters.
This can be a script step like:
```javascript 
(function execute(inputs, outputs) {
    e = JSON.parse(inputs.email_body);
    gs.info("Processing email:"+inputs.email_subject+"("+e.text+")");
    outputs.href = e.href;
    outputs.text = e.text;
    outputs.device = e.device;
})(inputs, outputs);
```

## Create an Incident
Assign the description and short description to <device>-<text>

## Update MPA with Incident number
Invoke the REST request created above, using the incident number returned.

## Log the result.



## 