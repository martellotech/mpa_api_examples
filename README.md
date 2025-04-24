**Sample Project: Use the Mitel Performance Analytics API to Integrate with Service Now**

To help you understand the capabilities of the Alarm API, this section walks you through a sample project that integrates Mitel Performance Analytics with ServiceNow. The project uses the REST API to retrieve alarms from MPA and then applies rules that allow you to create ServiceNow incidents using four different methods:

- Create an incident from an MPA alarm using the Favourites (star) button in the MPA interface.
- Create a service now incident for specific alarm text.
- Create an incident for an alarm and assign it to a user from within MPA.
- Create an incident for each critical alarm that is less than 1 hour old.

Hyperlinks are provided in both the MPA device dashboard and the ServiceNow incident for easy navigation between the two applications. 

This sample project is designed to run in a development environment only; do not implement it in a production environment.

**Before you Begin**

This project uses Visual Studio Code with a Python virtual environment. Ensure that the development machine you use for this project has Python version 3 installed. 

You also need to have the following:

- Access to an MPA system in a development environment, such as a lab system or a non-production staging system, with System Administrator privileges.
- The IP address of a non-production device.
- Access to  https://github.com/martellotech/mpa\_api\_examples.git
- Credentials for an MPA account that can be used by the API. You can create an account for the purposes of this example, such as "mpa\_api@yourdomain.com," or use an existing account.
- Credentials for a ServiceNow account that can be used to create new incidents. You can create an account such as "mpa\_api@yourdomain.com" or use an existing account.

**Configure the API**

1. Create an MPA container that you can use for testing.
1. From the root level of the container, select **System Administration > License Pool** and copy the Container GUID. You will need the GUID when you configure the API.
1. Select **System Administration > New Device**.
1. From the **Device Type** list, select **Basic IP Device**. Complete the following fields and click **Save**:
   1. ` `Name—Enter a name for your test device.  
   1. ` `Probe—Ensure this field is set to Disabled (the default setting). This will raise a No Probe Configured alarm that you can use for test purposes. 
   1. ` `Description—Enter a description, such as “ServiceNow test.” 
   1. ` `IP Address/FQDN—Enter the IP address of a non-production device.
1. Open a new** Visual Studio Code** session**.** 
1. Use the following command to clone the project repository:
   1. git clone git@github.com:martellotech/mpa\_api\_examples.git
1. Open the project in your workspace by clicking **File> Open Folder** and selecting the folder where the cloned repository was saved.
1. Press **CTRL-Shift-P** to create a Python virtual environment. When you are prompted to choose the files to include in the environment, include **requirements.txt**.
1. Select the Python Interpreter**.** For this project, you can select either Venv or Conda.** 
1. In the working directory, create a .env file by executing the following commands:

   python api/API\_Config.py

1. When you are prompted, enter the following information:
- **MPA\_HOST**—The FQDN of your MPA system.
- **MPA\_UID**—The MPA user ID you will use for the API. 
- **MPA\_PW**—The password for the MPA account.
- **MPA\_CONTAINER**—The GUID for the test container.
- **SNOW\_HOST**—The FQDN of your ServiceNow system.
- **SNOW\_UID**—The ServiceNow user ID that will be used to create new incidents.
- **SNOW\_PW**—The password for the ServiceNow account.

1. Select the file named MPA\_TO\_SNOW.py and choose **Run > Start Without Debugging** from the menu.

**Test the Integration**

Complete the followPing steps to test the three methods of creating ServiceNow incidents based on MPA alarms.

1. In the MPA test container, locate the **No Probe Configured** alarm in the Alarms table and click the **Favourite** (star) icon. In approximately 15 seconds, you will see a ServiceNow incident number populated in the table.
1. Create a probe called “SNOW Probe”.   This probe will raise a “Probe has not yet connected alarm”.   This alarm will be given a SNOW incident with a navigation link back to MPA to download and connect the probe.  This alarm text is in the file “mpa\_to\_snow\_mapping.xlsx”.   Any text in the MPA column that matches an alarm will create a SNOW inicident with the indicated text and comment.
1. To test assigning a user to a ServiceNow incident from within MPA, create an alarm and asign a user to it.   For example, on the probe created above, configure Basic IP SLA for an address that doesn’t exist on the probe’s network, and set the Basic IP SLA threshold to raise a critical alarm.   When this alarm appears, assign it to a user.   Within 15s you should see a service now incident created for the alarm.
