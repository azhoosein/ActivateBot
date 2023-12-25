class Activation:

    def __init__(self, activation_id, imei_number, sim_eid, plan_name, status, zip_code, addon_name, sim_type, requestor_id, firstname, lastname, email, amount, selected_plan, selected_addon):
        self.activation_id = activation_id
        self.imei_number = imei_number
        self.sim_eid = sim_eid
        self.plan_name = plan_name
        self.status = status
        self.zip_code = zip_code
        self.addon_name = addon_name
        self.sim_type = sim_type
        self.requestor_id = requestor_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.amount = amount
        self.selected_plan = selected_plan
        self.selected_addon = selected_addon

    def __str__(self):
        return f"""Activation ID: {self.activation_id}
imei_number: {self.imei_number}
sim_eid: {self.sim_eid}
plan_name: {self.plan_name}
status: {self.status}
zip_code: {self.zip_code}
addon_name: {self.addon_name}
sim_type: {self.sim_type}
requestor_id: {self.requestor_id}
firstname: {self.firstname} 
lastname: {self.lastname}
email: {self.email} 
amount: {self.amount}
selected_plan: {self.selected_plan}
selected_addon: {self.selected_addon}"""
    

class Logins:

    def __init__(self, id, tmobile_user, tmobile_password, epay_user, epay_password):
        self.id = id
        self.tmobile_user = tmobile_user
        self.tmobile_password = tmobile_password
        self.epay_user = epay_user
        self.epay_password = epay_password

    
# TEST USER | new = Activation(1023, 35253535354, 89021423243, "50TEXT", "New", 77036, "MC", "SIM", "8xdfasf3", "Test", "User", "Testuser@gmail.com", 55, "50prepaid", "Mexico & Canada")
