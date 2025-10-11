# USE CASE DESCRIPTION
| Use Case 1: | Create a Science Plan | 
|-------------|-----------------------|
| Use Case Name:     | Create a Science Plan | 
| Actor(s):          | Researcher, Scientist  | 
| Pre-condition:     | The user is logged into the system. |  
| Description:       | The user creates a new science plan by specifying the title, research goals, and the basic framework for the research project. |
| Basic Flow:        | 1. User logs into the system.|
|                    | 2. User selects the option to "Create Science Plan."|
|                    | 3. User enters the title of the plan.|
|                    | 4. User defines the research goals and key objectives of the plan.|
|                    | 5. User saves the plan and moves to the next phase of plan development. |
| Post-condition:  | A new science plan is created and saved in the system. |
| Alternative Flow: | If required fields are missing, the system prompts the user to fill in the necessary information. |

| Use Case 2 | Add Science Plan | 
| -----------|------------------|
| Use Case Name | Add Science Plan |
| Actor(s) | Researcher, Scientist, Administrator |
| Pre-condition | The user is logged into the system, and a science plan has been created. |
| Description | The user adds more details to the science plan, such as research methods, resources, and a timeline for completing tasks. |
| Basic Flow | 1.User selects the "Add Science Plan" option.|
|            | 2.User uploads any additional documents or supporting data.|
|            | 3.User defines the research methods, resources, and budget allocation.|
|            | 4.User sets the project milestones and timelines.|
|            | 5.User saves the plan.|
| Post-condition | The science plan has additional details saved to the system.|
| Alternative Flow | If any field is left incomplete or an invalid file is uploaded, the system notifies the user to correct it.|

| Use Case 3 | Update Science Plan |
|------------|---------------------|
| Use Case Name | Update Science Plan |
| Actor(s) | Researcher, Scientist, Project Manager |
| Pre-condition | The user has created or added a science plan that is in progress. |
| Description | The user updates an existing science plan by modifying details like goals, methods, timeline, or resources, based on changes or new findings. |
| Basic Flow | 1. User selects the science plan to be updated from the dashboard. |
|            | 2. User reviews the existing plan.|
|            | 3. User updates any necessary fields such as goals, methods, or timeline.|
|            | 4. User saves the updated plan.|
| Post-condition | The science plan is updated with the new information.|
| Alternative Flow | If the user tries to save invalid data or misses essential fields, the system prompts them to fill in the missing or correct details. |

| Use Case 4 | Cancel Science Plan and Storage |
|------------|---------------------------------|
| Use Case Name | Cancel Science Plan and Storage |
| Actor(s) | Researcher, Scientist, Project Manager |
| Pre-condition | The user has an active science plan stored in the system.|
| Description |  The user cancels the science plan, removes it from active status, and deletes any associated storage, documents, or resources.|
| Basic Flow | 1. User selects the "Cancel Science Plan" option.|
|            | 2. User confirms the cancellation by reviewing the plan’s status and associated documents.|
|            | 3. User chooses to either archive or delete any stored resources or documents associated with the plan.|
|            | 4. User finalizes the cancellation.|
| Post-condition | The science plan is canceled, and associated data is either archived or deleted from the system.|
| Alternative Flow | If the user attempts to cancel without confirming the consequences (such as data deletion), the system prompts them for confirmation.|

| Use Case 5 | Test Science Plan |
|------------|-------------------|
| Use Case Name | est Science Plan |
| Actor(s) | Researcher, Scientist, Project Manager |
| Pre-condition | The science plan has been defined with all necessary components, including research methods and resources.|
| Description | The user tests the feasibility and effectiveness of the science plan by running simulations, small-scale experiments, or mock trials to validate assumptions before full implementation. |
| Basic Flow | 1. User selects the "Test Science Plan" option.|
|            | 2. User initiates small-scale tests, simulations, or trials based on the plan.|
|            | 3. User analyzes the results of these tests.|
|            | 4. User modifies the science plan if necessary, based on test results.|
|            | 5. User finalizes the plan for full implementation if tests are successful.|
| Post-condition | The science plan is either validated for implementation or revised based on test feedback.|
| Alternative Flow | If the test results are unsuccessful, the system recommends adjustments or further testing.|



