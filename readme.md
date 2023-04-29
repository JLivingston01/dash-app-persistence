## Dash App Refresh Persistence

Dash is useful for a python developer quickly prototyping a dashboard or simple application. For hierarchical or nested workflows, it can be difficult to accomplish the vision of the application in Dash. This is a project to develop strategies for nested or hierarchical workflows that are preserved in session memory through browser refreshes.  
  
The purpose of this project is to use Dash to allow users to  
  
1. Create tabs as desired  
2. Delete specific tabs  
3. Refresh the application and have the state of tabs created and destroyed preserved  
  
Here the dcc.Store component is used to store tab elements, as well as other data that needs persistence.  
  
Next steps to enhance usability, users should:  
  
4. Have editable content living on individual tabs preserved through refresh.  
  
To achieve (4), this may involve multiple instances of the dcc.Store, residing on created Tabs, with pattern-matching IDs.
