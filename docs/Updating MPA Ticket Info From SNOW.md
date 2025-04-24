# Updating MPA Ticket Info From SNOW

## Overview

To set the ticket info in MPA so that it links to a SNOW incident, SNOW should invoke the MPA REST API, providing the ticket information.
In this example, we process incoming emails from MPA.  For each alarm in the email, we create an incident.  We then extract the href field from the alarm, and use it to construct an http PUT to href/updateTicket.

## Create A REST Message in SNOW.

We create an outbound REST message in SNOW.  Select "Outbound->REST Message" from the "All" Menu, and pick the "New" Button.
<img src="./SNOW REST/Create MPA Update Ticket Information Message.PNG">

We add the "Default PUT" method with content that looks like:
```JSON
{
    "ticket": {
        "status": "Assigned",
        "assignee": {
            "name": "Doug Bellinger",
            "email": "dbellinger@martellotech.com",
            "GUID": "e7ed5481-6373-4e5d-9027-32b3534fdd0c"
        },
        "ticketinfo": {
            "number": "x",
            "URL": "y"
        }
    }
}
```

The Authentication profile "DougMPA" by pressing the Search button next to "Basic auth Profile" and choosing "New".
<img src="./SNOW REST/Choose Auth Profile.PNG">

Do test runs on this to prove that you've got the JSON content and Authentication correct.  

## Create an MPA Inbound Mail WorkFlow.

Choose New from the Flows view in [Workflow Studio](https://ven04612.service-now.com/now/workflow-studio/home/flow).

<img src="./SNOW REST/MPA Inbound Mail Flow.png">
### Trigger
Pick Inbound Email trigger, and configure it to process all messages from your MPA system. In this example "alarms@mw5-init.sipseller.net"

<img src="./SNOW REST/Inbound Mail Trigger.PNG">

### Extract MPA Parameters
Pull email_body and email_subject from the email.


### Create an Incident
<img src="./SNOW REST/Create Inicident.PNG">
extract href and incident number for use in the update.

### Update MPA...
Create an action, pass it href and incident_number
In the script step, invoke the rest message we created earlier.  This example sets the incident:
```javasript
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
This example would benefit from checking error conditions on the response status code.   For example, if credentials change, this flow will lock the user account out by repeatedly failing authentication.

### Test and Activate the Flow.

### Create an MPA Alert Profile that sends to SNOW

#### Create a Template
Like this:
<img src="./SNOW REST/MPA email template for SNOW.PNG">

#### Use the Template in an Alert Profile
Like this:
<img src="./SNOW REST/Alert Profile.PNG">
(Enable or Disable it)
