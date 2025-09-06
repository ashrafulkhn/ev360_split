# Steps for Integrating First Charging Session (PECC-WS)

## Step 1: Review and Plan Data Flow
- Confirm how `ModuleDataModel` stores and updates voltage/current for each module.
- Identify how guns are mapped to modules (`AssignedModules` per gun).
- Review how info/status messages are constructed and sent via WebSocket.

## Step 2: Expose Real-Time Module Data
- Ensure `ModuleDataModel.read_module_data` is accessible to the WebSocket server and handlers.
- Plan a function to aggregate voltage/current for each gun from its assigned modules.

## Step 3: Update Info/Status Message Logic
- Modify the info/status message builder to include the latest measured voltage/current for each gun.
- Ensure periodic updates are sent to SECC as required by the protocol.

## Step 4: Handle Charging Requests
- On receiving a cable check or `targetValues` request:
  - Update the demand dictionary for the gun.
  - Assign required modules to the gun and update `AssignedModules`.
  - Start/manage module threads for reading parameters.

## Step 5: Charging State Management
- On `chargingState="charge"`, begin charging phase and update info/status messages.
- On `chargingState="postCharge"`, set voltage/current to 0, reset modules, and send final info/status.

## Step 6: Session and Connection State
- Track EV connection state and update info messages accordingly.

## Step 7: Testing and Validation
- Test the full flow: SECC connects, requests charging, cable check, target values, charging, post-charge, reset.
- Validate info/status messages reflect real-time module data.
